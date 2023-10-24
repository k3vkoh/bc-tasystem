from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from .models import CustomUser


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfully')
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'update.html'
    success_url = reverse_lazy('home')
