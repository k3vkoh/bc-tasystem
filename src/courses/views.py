from django.views import View
from django.shortcuts import render, redirect
from .models import Course
from django.contrib.auth.mixins import LoginRequiredMixin
from openpyxl import load_workbook

class MyView(View):
    def get(self, request):
        return render(request, 'course_list/upload.html')

    def post(self, request):
		if request.FILES['excel_file']:
        	excel_file = request.FILES['excel_file']
        	workbook = load_workbook(excel_file)
        	sheet = workbook.active

	        for row in sheet.iter_rows(values_only=True):
	            if row[0] == 'Term':
	                continue
	            new_class = Course(term=row[0], 
	                                    class_type=row[1], 
	                                    course=row[3], 
	                                    section=row[4], 
	                                    course_title=row[5], 
	                                    instructor_first_name=row[6].split(',')[1],
	                                    instructor_last_name=row[6].split(',')[0],
	                                    room_name=row[7],
	                                    author=request.user,
	                                    timeslot=row[8],
	                                    max_enroll=row[9],
	                                    room_size=row[10],
	                                    num_tas=int(row[9])//20,
	                                    description=row[10]
	                                )
	            new_class.save()

        	return render(request, 'success.html')
        return render(request, 'upload.html')

