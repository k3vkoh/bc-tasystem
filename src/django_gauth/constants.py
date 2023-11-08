from bcta import settings

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET

BASE_URI = 'http://127.0.0.1:8000'

GOOGLE_REDIRECT_URI = f"{BASE_URI}/oauth/google/callback"
GOOGLE_SCOPES = "https://www.googleapis.com/auth/userinfo.email"
GOOGLE_LOGIN_REDIRECT_URI = (f"https://accounts.google.com/o/oauth2/v2/auth?"
                             f"response_type={'code'}"
                             f"&scope={GOOGLE_SCOPES}"
                             f"&access_type={'offline'}"
                             f"&include_grant_scopes={'true'}"
                             #  f"&state={ <SESSION STATE> }"
                             f"&client_id={GOOGLE_CLIENT_ID}"
                             f"&redirect_uri={GOOGLE_REDIRECT_URI}")
