import google_auth_oauthlib
from django.conf import settings
from googleapiclient.discovery import build

class GoogleCalenderUtils:
    @staticmethod
    def get_oauth2_flow(scopes, redirect_uri):
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.CLIENT_SECRET_FILE,
            scopes=scopes
        )

        flow.redirect_uri = redirect_uri
        return flow

    @staticmethod
    def get_event_list(credentials):
        service = build('calendar', 'v3', credentials=credentials)
        calendar_list = service.calendarList().list().execute()
        event_list = []

        for calendar in calendar_list.get('items', []):
            calendar_id = calendar['id']
            events = service.events().list(calendarId=calendar_id).execute()
            event_list.extend(events.get('items', []))
        return event_list