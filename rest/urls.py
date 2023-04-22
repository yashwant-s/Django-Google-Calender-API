from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('v1/calendar/init/', GoogleCalendarInitView.as_view(), name = 'authorization_view'
),
    path('v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name = 'calender_view')

    ]