from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .forms import CustomUserUpdateForm
from .models import CustomUser


class ProfileView(UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = 'update.html'
    success_url = reverse_lazy('home')
