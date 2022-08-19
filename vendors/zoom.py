import json

import arrow
import requests
from requests.exceptions import HTTPError

from django.conf import settings


class Zoom(object):
    BASE_URL = "https://api.zoom.us/v2"

    def __init__(self):
        self.headers = {
            "authorization": f"Bearer {settings.ZOOM_JWT}",
            "content-type": "application/json",
        }

    def list_users(self):
        url = self.BASE_URL + "/users"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_user_account(self, proxy_email_address, first_name, last_name):
        """
        Given a proxy email address, make a Zoom user account and return the ID
        """
        payload = {
            "action": "custCreate",
            "user_info": {
                "email": proxy_email_address,
                "first_name": first_name,
                "last_name": last_name,
                "type": 1,
                "feature": {"zoom_phone": False},
            },
        }

        url = self.BASE_URL + "/users"

        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
        except HTTPError as e:
            # user already exists
            if response.json().get("code") == 1005:
                return self.get_user_id(proxy_email_address)

        return response.json().get("id")

    def get_user_id(self, proxy_email_address):
        """
        Returns an id for the zoom user given the proxy email address
        """
        url = self.BASE_URL + f"/users/{proxy_email_address}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("id")

    def list_meetings(
        self,
        proxy_email_address,
    ):
        """
        Returns a list of dictionaries representing meetings for the given user
        """
        url = self.BASE_URL + f"/users/{proxy_email_address}/meetings"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json().get("meetings")

    def get_meeting(self, zoom_meeting_id):
        """
        Returns detailed information about the given meeting. This is necessary because it's the only way to get the start and
        join urls
        """
        url = self.BASE_URL + f"/meetings/{zoom_meeting_id}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_meeting(
        self,
        proxy_email_address,
        patient_email_address,
        appointment_id,
        duration,
        timezone="America/Denver",
    ):
        """
        Creates a Zoom meeting to represent an Appointment
        """
        # these are the timezones we need for Zoom
        # [
        #     "America/Los_Angeles",
        #     "Pacific/Honolulu",
        #     "America/Anchorage",
        #     "America/Denver",
        #     "America/Chicago",
        #     "America/New_York",
        # ]

        start_time = (
            arrow.utcnow().to(timezone).shift(hours=1).strftime("%Y-%m-%dT%H:%M:%S")
        )

        payload = {
            "default_password": False,
            "duration": duration,
            "pre_schedule": False,
            "schedule_for": proxy_email_address,
            "settings": {
                "allow_multiple_devices": True,
                "auto_recording": "cloud",
                # "calendar_type": 1,
                "email_notification": True,
                "encryption_type": "enhanced_encryption",
                "focus_mode": True,
                "global_dial_in_countries": ["US"],
                "jbh_time": 0,
                "join_before_host": False,
                # TODO: add me
                # "meeting_invitees": [{"email": patient_email_address}],
                "meeting_invitees": [],
                "mute_upon_entry": False,
                "participant_video": False,
                "private_meeting": False,
                "registrants_confirmation_email": True,
                "registrants_email_notification": True,
                "waiting_room": True,
                "watermark": False,
            },
            "start_time": start_time,
            "timezone": timezone,
            # "tracking_fields": [
            #     {
            #         "telepsycrx_appointment_id": str(appointment_id),
            #     }
            # ],
            # scheduled single meeting
            "type": 2,
        }

        url = self.BASE_URL + f"/users/{proxy_email_address}/meetings"

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()

        meeting_id = response.json().get("id")
        meeting_details = self.get_meeting(meeting_id)

        meeting_details = dict(
            id=meeting_id,
            start_url=meeting_details.get("start_url"),
            join_url=meeting_details.get("join_url"),
        )

        return meeting_details
