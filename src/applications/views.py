from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Application
from courses.models import Course
from .forms import ApplicationForm

class ApplicationCreateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Application
    template_name = 'application_form.html'
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_object()
        return context
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()
    

class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        return Application.objects.filter(student=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_student():
            context['title'] = 'My Applications'
            context['applications'] = self.get_queryset().filter(student=self.request.user)
        else:
            context['title'] = 'Applications'
            context['applications'] = self.get_queryset().filter(course__professor=self.request.user)
        
        return context
    

    
    

        

