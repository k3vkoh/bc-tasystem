from django.views import View
from django.shortcuts import render, redirect
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from openpyxl import load_workbook
from users.models import CustomUser as User
from random import randint
from django.views.generic import ListView, DetailView

class UploadView(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        excel_file = request.FILES.get('excel_file')
        if excel_file:
            self.process_excel_file(excel_file)
            return render(request, 'success.html')
        return render(request, 'upload.html')
    
    def process_excel_file(self, excel_file):
        workbook = load_workbook(excel_file)
        sheet = workbook.active

        for row in sheet.iter_rows(values_only=True):
            if not row[0] or row[0] == 'Term': 
                continue
            instructor = self.get_or_create_instructor_from_row(row)
            self.create_course(row, instructor)
    
    def get_or_create_instructor_from_row(self, row):
        instructor_first_name = row[6].split(',')[1].strip()
        instructor_last_name = row[6].split(',')[0].strip()
        
        instructor, created = User.objects.get_or_create(
            first_name=instructor_first_name,
            last_name=instructor_last_name,
            defaults={
                'professor': True,
                'password': 'password',  # TODO: Make sure to change this
                'email': f"{instructor_last_name.lower()[:4]}@bc.edu",  # TODO: Change this to a valid email
                'eagleid': self.generate_eagleid()
            }
        )
        return instructor

    def create_course(self, row, instructor):
        new_class = Course.objects.create(
            term=row[0],
            class_type=row[1],
            course=row[3],
            section=row[4],
            course_title=row[5],
            instructor_first_name=instructor.first_name,
            instructor_last_name=instructor.last_name,
            room_name=row[7],
            timeslot=row[8],
            max_enroll=row[9],
            room_size=row[10],
            num_tas=int(row[9]) // 20,
            description=row[12],
            professor=instructor
        )
        instructor.courses.add(new_class)
    
    def generate_eagleid(self):
        eagleid = randint(10000000, 99999999)
        while User.objects.filter(eagleid=eagleid).exists():
            eagleid = randint(10000000, 99999999)
        return eagleid
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

class ListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'list.html'
    ordering = ['course']
    context_object_name = 'course_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
