from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from . import constants
from django.contrib.auth import authenticate, login
from .backends import GoogleAuthBackend
from django.contrib import messages


def google_login(request):
    return HttpResponseRedirect(constants.GOOGLE_LOGIN_REDIRECT_URI)


def google_callback(request):
    if 'error' in request.GET:
        return redirect('home')

    if 'code' in request.GET:
        user = authenticate(request, code=request.GET.get(
            'code'), backend=GoogleAuthBackend)
        if user:
            login(request, user=user)
        else:
            messages.error(request, "You are not Authorized to Login ")
        return redirect('home')
