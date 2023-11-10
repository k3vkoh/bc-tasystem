from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Application
from courses.models import Course
from .forms import ApplicationForm
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from offers.views import send_html_email


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
        context['can_apply'] = self.ensure_user_can_apply()
        return context

    def get_success_url(self):
        # email for the professor after the student submits application
        url = reverse('courses:course-detail', args=[self.get_object().id])
        subject = f'TA Offer Update For {self.get_object().instructor_first_name} {self.get_object().instructor_last_name}'
        message = [f'Dear {self.get_object().instructor_first_name} {self.get_object().instructor_last_name}',
                   f'The student submitted an application for {self.get_object().course_title}. View the application here: https://cscita.bc.edu{url}']
        # recipients = self.get_object().professor.email # for production
        recipients = 'kohke@bc.edu'  # for testing purposes
        send_html_email(subject, recipients, message)
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
        application = self.get_object()
        if application.get_status() != "PENDING":
            return False
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


class ApplicationRejectView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Application
    fields = []
    template_name = 'application_reject.html'
    success_message = "The application has been rejected successfully!"

    def form_valid(self, form):
        self.object.reject()
        return super().form_valid(form)

    def get_success_url(self):
        # email for the student after an application is rejected
        url = reverse('courses:course-list')
        subject = f'TA Application Update For {self.get_object().student.first_name} {self.get_object().student.last_name}'
        message = [f'Dear {self.get_object().student.first_name} {self.get_object().student.last_name}',
                   f'We regret to inform you that your application has been rejected. You can view other courses here: https://cscita.bc.edu{url}']
        # recipients = self.get_object().student.email # for production
        recipients = 'kohke@bc.edu'  # for testing purposes
        send_html_email(subject, recipients, message)
        return reverse('applications:application-list')

    def test_func(self):
        application = self.get_object()
        if application.get_status() != "PENDING":
            return False
        return self.request.user.is_superuser or self.request.user == self.get_object().course.professor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_object().course
        return context
