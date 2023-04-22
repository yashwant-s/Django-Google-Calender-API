from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .config import GOOGLE_CALENDAR_SCOPES, GOOGLE_CALENDAR_REDIRECT_URI
from .utils import GoogleCalenderUtils


class GoogleCalendarInitView(APIView):

    def get(self, request):
        scopes = GOOGLE_CALENDAR_SCOPES
        redirect_uri = GOOGLE_CALENDAR_REDIRECT_URI
        flow = GoogleCalenderUtils.get_oauth2_flow(scopes, redirect_uri)

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        return redirect(authorization_url)



class GoogleCalendarRedirectView(APIView):
    def get(self, request):
        response_data = {
            'data':None,
            'errors':None
        }
        response_status = status.HTTP_200_OK
        error=request.query_params.get('error', None)

        if(error):
            response_data['errors']=error
        else:

            scopes = GOOGLE_CALENDAR_SCOPES
            redirect_uri = GOOGLE_CALENDAR_REDIRECT_URI
            try:
                code = request.query_params.get('code')
                flow=GoogleCalenderUtils.get_oauth2_flow(scopes, redirect_uri)

                flow.fetch_token(code=code)
                credentials=flow.credentials
                event_list=GoogleCalenderUtils.get_event_list(credentials)
                response_data['data']={'events':event_list,}
            except Exception as e:
                response_data['errors']=str(e)
                response_status=status.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(response_data, response_status,)