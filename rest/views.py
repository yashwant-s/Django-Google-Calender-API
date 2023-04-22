from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .config import GOOGLE_CALENDAR_SCOPES, GOOGLE_CALENDAR_REDIRECT_URI
from .utils import GoogleCalenderUtils


class GoogleCalendarInitView(APIView):
    """
    Initiates the Google Calendar authorization flow.

    This view initiates the OAuth2 authorization flow for Google Calendar API.
    The user is redirected to the Google authorization page to grant permissions.
    After successful authorization, the user is redirected to the redirect URI.

    """
    def get(self, request):
        """
        Handles the GET request for initiating the Google Calendar authorization flow.

        Returns:
            redirect: Redirects the user to the Google authorization page.

        """
        scopes = GOOGLE_CALENDAR_SCOPES  # Set the scopes for Google Calendar API
        redirect_uri = GOOGLE_CALENDAR_REDIRECT_URI  # Set the redirect URI for OAuth2 flow
        flow = GoogleCalenderUtils.get_oauth2_flow(scopes, redirect_uri)  # Create an OAuth2 flow

        # Get the authorization URL and state for offline access with granted scopes
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        return redirect(authorization_url)  # Redirect the user to the authorization URL


class GoogleCalendarRedirectView(APIView):
    """
    Handles the redirect from the Google Calendar authorization page.

    This view handles the callback from the Google authorization page after the user grants
    permissions. It fetches the access token and credentials, and uses them to retrieve the
    list of events from the Google Calendar API.

    """
    def get(self, request):
        """
        Handles the GET request for the Google Calendar authorization callback.

        Returns:
            Response: Returns the response with data and status.

        """
        response_data = {
            'data': None,
            'errors': None
        }
        response_status = status.HTTP_200_OK
        error = request.query_params.get('error', None)  # Check if there is an error in the query parameters

        if error:
            response_data['errors'] = error  # Set the error in the response data
        else:
            scopes = GOOGLE_CALENDAR_SCOPES  # Set the scopes for Google Calendar API
            redirect_uri = GOOGLE_CALENDAR_REDIRECT_URI  # Set the redirect URI for OAuth2 flow
            try:
                code = request.query_params.get('code')  # Get the authorization code from the query parameters
                flow = GoogleCalenderUtils.get_oauth2_flow(scopes, redirect_uri)  # Create an OAuth2 flow

                flow.fetch_token(code=code)  # Fetch the access token and credentials
                credentials = flow.credentials  # Get the credentials for accessing Google Calendar API
                event_list = GoogleCalenderUtils.get_event_list(credentials)  # Get the list of events using the credentials
                response_data['data'] = {'events': event_list, }  # Set the events data in the response data
            except Exception as e:
                response_data['errors'] = str(e)  # Set the error message in the response data
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR  # Set the response status to internal server error

        return Response(response_data, response_status,)  # Return the response with data and status
