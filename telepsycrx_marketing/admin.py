from django.contrib import admin
from .models import PatientWaitList, DoctorWaitList, UserReview, UserSuggestion


admin.site.register(PatientWaitList)
admin.site.register(DoctorWaitList)
admin.site.register(UserSuggestion)
admin.site.register(UserReview)