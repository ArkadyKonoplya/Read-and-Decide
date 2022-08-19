from rest_framework import serializers
# from rest_framework.request import Request
from notes.models import ProviderNote


class ProviderNoteSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="provider-notes-detail")

    class Meta:
        model = ProviderNote
        fields = ('url',
                  'id',
                  'author',
                  'patient',
                  'session_date',
                  'session_time',
                  'note',
                  'archived')
        # extra_kwargs = {
        #     'id': {
        #         'read_only': False, 
        #         'required': True
        #      }
        # }

    # def update(self, instance, validated_data):
    #     # Update the  instance
    #     instance.some_field = validated_data['some_field']
    #     instance.save()

    #     # Delete any detail not included in the request
    #     providerNote_ids = [item['note_id'] for item in validated_data['provider_notes']]
    #     for providerNote in ProviderNote.objects.all():
    #         if providerNote.id not in providerNote_ids:
    #             providerNote.delete()

    #     # Create or update providerNote 
    #     for providerNote in validated_data['notes']:
    #         providerNoteObj = ProviderNote.objects.get(pk=ProviderNote['id'])
    #         if providerNoteObj:
    #             providerNoteObj.some_field=ProviderNote['note']
    #             # ....fields...
    #         else:
    #            providerNoteObj = ProviderNote.create(car=instance,**providerNote)
    #         providerNoteObj.save()

    #     return instance
