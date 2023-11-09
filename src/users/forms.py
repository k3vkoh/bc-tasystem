from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser


class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['eagleid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']
