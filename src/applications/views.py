from typing import Any
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Application
from courses.models import Course
from .forms import ApplicationForm

class ApplicationCreateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Application
    template_name = 'application.html'
    form_class = ApplicationForm
    success_message = "Your application has been submitted successfully!"

    def form_valid(self, form):
        form.instance.student = self.request.user
        form.instance.course = self.get_object()
        return super().form_valid(form)
    
    def get_object(self):
        return Course.objects.get(pk=self.kwargs.get('pk'))
    
    def test_func(self):
        return self.request.user.is_student() or self.request.user.is_superuser
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_object()
        return context
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()
    
    

        

