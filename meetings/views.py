import arrow
import json
import math
import boto3
import requests
import threading
import logging

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .models import Meeting, RecordingStatus
from .serializers import MeetingSerializer, CreateMeetingSerializer
from zoomus import ZoomClient
from datetime import datetime


logger = logging.getLogger(__name__)


# class MeetingViewSet(viewsets.ModelViewSet):
#     queryset = Meeting.objects.all().order_by("date")
#     serializer_class = MeetingSerializer
#     filterset_fields = ["doctor", "patient"]
#     # permission_classes = (permissions.IsAuthenticated)

#     def create(self, request, *args, **kwargs):
#         serializer = CreateMeetingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         appointment = serializer.validated_data.get("appointment")
#         if not appointment.is_confirmed:
#             return Response(
#                 "The appointment is not confirmed", status=status.HTTP_400_BAD_REQUEST
#             )

#         client = ZoomClient(
#             api_key=settings.ZOOM_API_KEY, api_secret=settings.ZOOM_API_SECRET
#         )
#         payload = {
#             "topic": "TelePsycRX Meeting",
#             "agenda": f"{appointment.doctor} and {appointment.patient} meeting",
#             "default_password": True,
#             "type": 2,
#             "start_time": appointment.date,
#             "duration": appointment.duration,
#             # 'timezone': appointment.doctor.timezone,  # [TODO]: Handle the timezone.
#             "settings": {
#                 "audio": "both",
#                 "auto_recording": "cloud",
#                 "email_notification": False,
#                 "host_video": True,
#                 "participant_video": False,
#                 "join_before_host": False,
#                 "meeting_authentication": False,
#                 "mute_upon_entry": True,
#                 "private_meeting": True,
#                 "waiting_room": False,
#             },
#         }
#         # [TODO]: Change 'appointment.doctor.email' for 'appointment.doctor.zoom_email'
#         response = client.meeting.create(user_id=appointment.doctor.email, **payload)

#         if response.status_code == 200 or response.status_code == 201:
#             # [TODO]: Make an API call to register the Patient to the meeting.
#             response = response.json()
#             serializer.save(
#                 doctor=appointment.doctor,
#                 patient=appointment.patient,
#                 zoom_id=response["id"],
#                 zoom_password=response["password"],
#                 date=response["start_time"],
#                 duration=response["duration"],
#                 recording_status=RecordingStatus.NOT_AVAILABLE,
#             )
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         return Response(response, status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk=None, *args, **kwargs):
#         partial = kwargs.pop("partial", False)
#         instance = get_object_or_404(Meeting, pk=pk)
#         serializer = MeetingSerializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)

#         new_start_time = serializer.validated_data.get("date")
#         new_duration = serializer.validated_data.get("duration")

#         if new_start_time or new_duration:
#             client = ZoomClient(
#                 api_key=settings.ZOOM_API_KEY, api_secret=settings.ZOOM_API_SECRET
#             )
#             response = client.meeting.update(
#                 id=instance.zoom_id,
#                 start_time=new_start_time,
#                 duration=new_duration,
#             )
#             if response.status_code == 200 or response.status_code == 204:
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)

#             return Response(response, status=status.HTTP_400_BAD_REQUEST)

#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def destroy(self, request, pk=None, *args, **kwargs):
#         instance = get_object_or_404(Meeting, pk=pk)
#         client = ZoomClient(
#             api_key=settings.ZOOM_API_KEY, api_secret=settings.ZOOM_API_SECRET
#         )
#         response = client.meeting.delete(id=instance.zoom_id)
#         if response.status_code == 200 or response.status_code == 204:
#             # Delete s3 recording?
#             return super(MeetingViewSet, self).destroy(request, pk, *args, **kwargs)

#         return Response(response, status=status.HTTP_400_BAD_REQUEST)


def handle_recording(meeting_id, data):
    meeting = Meeting.objects.get(pk=meeting_id)
    bucket = boto3.resource("s3").Bucket(settings.ZOOM_BUCKET_NAME)
    config = boto3.s3.transfer.TransferConfig(
        multipart_threshold=1024 * 20,
        max_concurrency=2,
        multipart_chunksize=1024 * 20,
        use_threads=True,
    )
    main_video_file = None

    logger.info(
        "[{}] Sending Recording to S3 (meeting {})".format(
            threading.get_ident(), meeting.appointment.id
        )
    )
    for recording_file in data["payload"]["object"]["recording_files"]:
        download_url = "{}/?access_token={}".format(
            recording_file["download_url"], data["download_token"]
        )
        file_path = "meeting-{}/recording-{}.{}".format(
            meeting.appointment.id,
            recording_file["id"],
            recording_file["file_extension"],
        )
        if file_path.endswith(".MP4"):
            main_video_file = file_path

        try:
            r = requests.get(download_url, stream=True)
            bucket.upload_fileobj(r.raw, file_path, Config=config)
        except:
            logger.warning(
                "[{}] Error while uploading the files to s3, reverting...".format(
                    threading.get_ident()
                )
            )
            meeting.recording_status = RecordingStatus.ERROR
            bucket.objects.filter(Prefix=f"meeting-{meeting.appointment.id}/").delete()
            return

    client = ZoomClient(
        api_key=settings.ZOOM_API_KEY, api_secret=settings.ZOOM_API_SECRET
    )
    response = client.recording.delete(meeting_id=meeting.zoom_id, action="delete")

    if response.status_code != 204:
        logger.warning(
            "[{}] Cannot delete zoom recording, reverting...".format(
                threading.get_ident()
            )
        )
        meeting.recording_status = RecordingStatus.ERROR
        bucket.objects.filter(Prefix=f"meeting-{meeting.appointment.id}/").delete()
    else:
        if not main_video_file:
            logger.warning("[{}] No MP4 file found".format(threading.get_ident()))
            meeting.recording_status = RecordingStatus.NOT_AVAILABLE
        else:
            meeting.recording_status = RecordingStatus.COMPLETED
            meeting.recording_url = "https://{}.s3.{}.amazonaws.com/{}".format(
                settings.ZOOM_BUCKET_NAME,
                settings.AWS_DEFAULT_REGION,
                main_video_file,
            )
    meeting.save()
    logger.info(
        "[{}] Recording transfer success (meeting {})".format(
            threading.get_ident(), meeting.appointment.id
        )
    )


@api_view(["POST"])
def recordingView(request):
    if request.headers.get("authorization") == settings.ZOOM_VERIFICATION_TOKEN:
        logger.info("Ok! Request Authorized")
        # logger.info(json.dumps(dict(request.data), indent=4)) # Uncomment for DEBUG
        data = dict(request.data)

        # TODO: defend against missing zoom id
        zoom_meeting_id = data["payload"]["object"]["id"]

        try:
            meeting = Meeting.objects.get(zoom_id=zoom_meeting_id)
        except Meeting.DoesNotExist:
            logger.error(f"recordingView: no meeting found for id {zoom_meeting_id}")
            return Response(
                "No meeting found with given ID",
                status=status.HTTP_404_NOT_FOUND,
            )
        except Meeting.MultipleObjectsReturned:
            logger.warning(
                f"recordingView: multiple meetings found for id {zoom_meeting_id}"
            )
            meeting = Meeting.objects.filter(zoom_id=zoom_meeting_id).first()

        if data.get("event") == "meeting.ended":
            start_time = arrow.get(data["payload"]["object"]["start_time"]).to(
                meeting.doctor.timezone
            )
            end_time = arrow.get(data["payload"]["object"]["end_time"]).to(
                meeting.doctor.timezone
            )

            meeting.session_start = start_time.datetime
            meeting.session_duration = math.ceil((end_time - start_time).seconds / 60)
            meeting.recording_status = RecordingStatus.PROCESSING
            meeting.save()

        elif data.get("event") == "recording.completed":
            t = threading.Thread(
                target=handle_recording,
                args=(
                    zoom_meeting_id,
                    data,
                ),
            )
            t.start()

        return Response(
            "Authorized request to TelePsycRX WebHook App",
            status=status.HTTP_200_OK,
        )
    else:
        logger.warning("Bad! Request Unauthorized")
        return Response(
            "Unauthorized request to TelePsycRX WebHook App",
            status=status.HTTP_200_OK,
        )
