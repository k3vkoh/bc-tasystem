from django.views import View
from django.shortcuts import render, redirect
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from openpyxl import load_workbook
from users.models import CustomUser as User
from random import randint

class UploadView(View):
	def get(self, request):
		return render(request, 'upload.html')

	def post(self, request):
		if request.FILES['excel_file']:
			excel_file = request.FILES['excel_file']
			workbook = load_workbook(excel_file)
			sheet = workbook.active

			for row in sheet.iter_rows(values_only=True):
				if not row[0]: break
				if row[0] == 'Term': continue

				instructor_first_name = row[6].split(',')[1].strip()
				instructor_last_name = row[6].split(',')[0].strip()

				# Check if a user with the given instructor's first name, last name, and professor=True exists.
				# If not, create one.
				instructor, created = User.objects.get_or_create(
					first_name=instructor_first_name,
					last_name=instructor_last_name,
					professor=True
				)

				if created:
					instructor.set_password('password')
					instructor.email = instructor_last_name.lower()[0:4] + '@bc.edu' # TODO: Change this to a valid email
					instructor.eagleid = self.generate_eagleid()
					instructor.save()


				new_class = Course(
					term=row[0], 
					class_type=row[1], 
					course=row[3], 
					section=row[4], 
					course_title=row[5], 
					instructor_first_name=instructor_first_name,
					instructor_last_name=instructor_last_name,
					room_name=row[7],
					timeslot=row[8],
					max_enroll=row[9],
					room_size=row[10],
					num_tas=int(row[9])//20,
					description=row[12],
					professor=instructor
				)
				new_class.save()

			return render(request, 'success.html')
		return render(request, 'upload.html')
	
	def generate_eagleid(self):
		eagleid = randint(10000000, 99999999)
		while User.objects.filter(eagleid=eagleid).exists():
			eagleid = randint(10000000, 99999999)
		print(eagleid)
		return eagleid

class ListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'list.html'
    ordering = ['course']
    context_object_name = 'course_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
