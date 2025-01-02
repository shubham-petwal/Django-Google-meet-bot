from django.shortcuts import render, redirect
from .models import Meeting
import subprocess
from . import main
from datetime import datetime
from .tasks import join_and_record_meeting_task
from django.utils.timezone import make_aware, now




# def index(request):
#     if request.method == "POST":
#         link = request.POST['link']
#         participant_name = request.POST['participant_name']
#         meeting_date = request.POST['date']  # Date in 'YYYY-MM-DD' format
#         meeting_time = request.POST['time']  # Time in 'HH:MM' format
#         meeting_datetime = datetime.strptime(f"{meeting_date} {meeting_time}", "%Y-%m-%d %H:%M")
#         print("THe date time is",meeting_datetime)
#         bot = main.MyBot()
#         data = bot.join_and_record_meeting(link)
#         print("the data is",data)
#         # Save meeting details
#         meeting = Meeting.objects.create(link=link, participant_name=participant_name, datetime=meeting_datetime,summary=data["summary"],transcription=data["transcript"])
#         # Start the bot (dummy subprocess example)
#         # subprocess.Popen(["python", "bot/main.py", link, str(duration)])

#         return redirect("meeting_summary", pk=meeting.pk)

#     return render(request, "bot/index.html")


def index(request):
    if request.method == "POST":
        link = request.POST['link']
        participant_name = request.POST['participant_name']
        meeting_date = request.POST['date']  # 'YYYY-MM-DD'
        meeting_time = request.POST['time']  # 'HH:MM'
        
        # Combine date and time, then make it timezone-aware
        meeting_datetime_naive = datetime.strptime(f"{meeting_date} {meeting_time}", "%Y-%m-%d %H:%M")
        meeting_datetime = make_aware(meeting_datetime_naive)

        # Save the meeting details
        meeting = Meeting.objects.create(link=link, participant_name=participant_name, datetime=meeting_datetime)

        # Calculate the delay in seconds
        delay_seconds = (meeting_datetime - now()).total_seconds()
        print("The delay in seconds is:", delay_seconds)
        # bot = main.MyBot()
        # bot.join_and_record_meeting(link)

        # Schedule the task
        join_and_record_meeting_task.apply_async(
            (link, participant_name, meeting.pk), 
            countdown=delay_seconds
        )
        
        return redirect("scheduledMeeting")

    return render(request, "bot/index.html")



def meeting_summary(request, pk):
    meeting = Meeting.objects.get(pk=pk)
    return render(request, "bot/summary.html", {"meeting": meeting})

def scheduledMeeting(request):
    return render(request,"bot/scheduled.html")

def meeting_history(request):
    allHistoryData = Meeting.objects.all()
    return render(request,'bot/meeting_history.html',{"meeting":allHistoryData})