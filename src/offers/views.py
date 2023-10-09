from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from applications.models import Application
from courses.models import Course
from .models import Offer


class OfferCreateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Offer
    template_name = 'offer_form.html'
    success_message = "Your offer has been submitted successfully!"
    fields = []

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.recipient = self.get_object().student
        form.instance.course = self.get_object().course
        form.instance.application = self.get_object()

        return super().form_valid(form)
    
    def get_object(self):
        return Application.objects.get(pk=self.kwargs.get('pk'))
    
    def test_func(self):
        return self.get_object().course.professor == self.request.user or self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = self.get_object()
        return context
    
    def get_success_url(self):
        return self.get_object().get_absolute_url()