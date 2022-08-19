from django.contrib import admin
from .models import Meeting


@admin.register(Meeting)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "appointment",
        "zoom_id",
    )
