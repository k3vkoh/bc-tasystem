from django.contrib.auth.backends import BaseBackend
from users.models import CustomUser
import requests
from django_gauth import constants

UserModel = CustomUser


class GoogleAuthBackend(BaseBackend):
    """Custom Backend Server for Google auth"""

    def _get_access_token(self, code):
        """
        Return access_toke from code
        :param code: google Code from callback
        :return: User Instance
        """

        response = requests.post('https://oauth2.googleapis.com/token', data={
            "code": code,
            "client_id": constants.GOOGLE_CLIENT_ID,
            'client_secret': constants.GOOGLE_CLIENT_SECRET,
            "redirect_uri": constants.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        })
        return response.json().get('access_token')

    def get_user(self, pk):
        """Returns a user instance """
        try:
            return UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            return None

    def authenticate(self, request, code=None, **kwargs):
        """
        Authentication function for Custom google token verification
        parms:
            code - Google code received form view
        """
        if code:
            access_token = self._get_access_token(code)
            if access_token:
                google_user_details = requests.get(
                    f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}')
                email = google_user_details.json().get('email')
                first_name = google_user_details.json().get('given_name')
                last_name = google_user_details.json().get('family_name')
                user = UserModel.objects.filter(email=email).first()
                if not user:
                    user = UserModel.objects.create_user(
                        email=email,
                        password=None,
                        professor=False,
                        first_name=first_name,
                        last_name=last_name,
                    )
                return user
