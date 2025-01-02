from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("meeting_history/",views.meeting_history, name = "meeting_history"),
    path("summary/<int:pk>/", views.meeting_summary, name="meeting_summary"),
    path("scheduled/", views.scheduledMeeting, name="scheduledMeeting"),
]
