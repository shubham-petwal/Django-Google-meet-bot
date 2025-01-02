from django.db import models
from datetime import datetime
class Meeting(models.Model):
    link = models.URLField()
    participant_name = models.CharField(max_length=255)
    datetime = models.DateTimeField(default=datetime.now)
    transcription = models.TextField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)