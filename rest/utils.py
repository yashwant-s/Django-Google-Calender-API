import google_auth_oauthlib
from django.conf import settings
from googleapiclient.discovery import build

class GoogleCalenderUtils:
    """
    Utility class for Google Calendar API operations.
    """
    @staticmethod
    def get_oauth2_flow(scopes, redirect_uri):
        """
        Creates an OAuth2 flow for Google Calendar API.

        Args:
            scopes (list): List of scopes to request access to.
            redirect_uri (str): Redirect URI for the OAuth2 flow.

        Returns:
            flow (google_auth_oauthlib.flow.Flow): The OAuth2 flow.

        """
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            settings.CLIENT_SECRET_FILE,  # Load client secrets file
            scopes=scopes  # Set the scopes for Google Calendar API
        )

        flow.redirect_uri = redirect_uri  # Set the redirect URI for the OAuth2 flow
        return flow  # Return the OAuth2 flow

    @staticmethod
    def get_event_list(credentials):
        """
        Retrieves a list of events from Google Calendar API.

        Args:
            credentials (google.oauth2.credentials.Credentials): User credentials for accessing Google Calendar API.

        Returns:
            event_list (list): List of events retrieved from the Google Calendar API.

        """
        service = build('calendar', 'v3', credentials=credentials)  # Build the Calendar API service
        calendar_list = service.calendarList().list().execute()  # Get the list of calendars
        event_list = []  # Initialize the list to store events

        for calendar in calendar_list.get('items', []):
            calendar_id = calendar['id']
            events = service.events().list(calendarId=calendar_id).execute()  # Get the events for each calendar
            event_list.extend(events.get('items', []))  # Extend the event list with the retrieved events

        return event_list  # Return the list of events