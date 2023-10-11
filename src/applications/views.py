from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Application
from courses.models import Course
from .forms import ApplicationForm
from django.urls import reverse
from django.contrib import messages


class ApplicationCreateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Application
    template_name = 'application_form.html'
    form_class = ApplicationForm
    success_message = "Your application has been submitted successfully!"

    def form_valid(self, form):
        error = self.ensure_user_can_apply()
        if error:
            messages.error(self.request, error)
            return super().form_invalid(form)
        form.instance.student = self.request.user
        form.instance.course = self.get_object()
        application = form.save()  
        course = self.get_object()  
        course.applications.add(application) 
        self.request.user.applications.add(application)
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

    def ensure_user_can_apply(self):
        user = self.request.user
        if user.is_professor():
            return "You cannot apply to a course if you are a professor"
        if user.reached_max_applications():
            return "You have reached the maximum number of courses you can apply to (5)"
        if user.already_applied_to_course(self.get_object()):
            return "You have already applied to this course"
        if user.is_ta():
            return "You are already a TA for a course"
        return None
    

    

class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'applications.html'
    context_object_name = 'applications'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Application.objects.all()
        elif self.request.user.is_student():
            return Application.objects.filter(student=self.request.user)
        else:
            return Application.objects.filter(course__professor=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = self.get_queryset()
        if self.request.user.is_student():
            context['title'] = 'My Applications'
        else:
            context['title'] = 'Applications'
        return context
    
class ApplicationDeleteView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Application
    template_name = 'application_confirm_delete.html'
    success_message = "Your application has been deleted successfully!"
    
    def get_success_url(self):
        return reverse('applications:application-list')
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().student
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_object().course
        return context\
        

class ApplicationDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Application
    template_name = 'application_detail.html'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().student or self.request.user == self.get_object().course.professor
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_object().course
        return context

        

