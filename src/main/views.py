from django.shortcuts import render
from courses.models import Course


def home(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'home.html', context)
