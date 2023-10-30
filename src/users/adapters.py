from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_email
from users.models import CustomUser as User
from allauth.account.models import EmailAddress

'''
This module is called when a user tries to login via a social account.
If the user already exists, connect the social account to the existing user.
If the user does not exist, create a new user with the social account details.
It is needed because allauth attempts to create a new user regardless of whether the user with an email already exists.

Basically, all of this is done to make sure that google oauth doesn't create a new user for each user that was already present in the database but was not created via google oauth. 

I still don't even understand this tbh but it works so I'm not gonna touch it. I tried to comment what I do know but I will forget very soon.

Without this, google oauth will create a new user for each user that was already present in the database but was not created via google oauth. This will raise a unique constraint error.
'''


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            try:
                existing_user = User.objects.get(email=user.email)
            except User.DoesNotExist:
                pass
            return
        if not user.email:
            return
        try:
            existing_user = User.objects.get(email=user.email)
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass

    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user
        # check if the user already exists by email
        try:
            existing_user = User.objects.get(email=user.email)
            return existing_user  # return the found user and do not continue creating the new one
        except User.DoesNotExist:
            user.save()  # save only if no user with that email exists
            return user

    def is_auto_signup_allowed(self, request, sociallogin):
        try:
            email_address = EmailAddress.objects.get(
                email=sociallogin.user.email)
            if email_address:
                # if the account exists, connect it automatically to the social account rather than do any other verifications
                sociallogin.connect(request, email_address.user)
                return False  # stop here since the user exists otherwise it will attempt to create a new user
        except EmailAddress.DoesNotExist:
            pass
        return super().is_auto_signup_allowed(request, sociallogin)
