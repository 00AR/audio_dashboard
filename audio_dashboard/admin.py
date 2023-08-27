from django.contrib import admin
from .models import Audio


class AudioAdmin(admin.ModelAdmin):
    pass


admin.site.register(Audio, AudioAdmin)
