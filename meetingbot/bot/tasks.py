from celery import shared_task
from . import main
from .models import Meeting

@shared_task
def join_and_record_meeting_task(link, participant_name, meeting_id):
    bot = main.MyBot()
    data = bot.join_and_record_meeting(link)
    print("Meeting data:", data)

    # Update the meeting record with the results
    meeting = Meeting.objects.get(pk=meeting_id)
    meeting.summary = data["summary"]
    meeting.transcription = data["transcript"]
    meeting.save()
