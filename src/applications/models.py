from django.db import models
from users.models import CustomUser as User
from courses.models import Course
from enum import Enum

class Status(Enum):
    '''
    Enum for the status of an application
    PENDING - The application has been submitted but not yet reviewed
    APPROVED - The application has been accepted by the professor
    REJECTED - The application has been rejected by the professor or the offer has been rejected by the student
    CONFIRMED - The application offer has been confirmed by the student
    '''
    PENDING = 1
    APPROVED = 2
    REJECTED = 3
    CONFIRMED = 4

class Application(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)

    additional_information = models.TextField(max_length=500, blank=True)
    status = models.IntegerField(choices=[(tag.value, tag.name) for tag in Status], default=Status.PENDING.value)

    def __str__(self):
        return self.student + " - " + self.course
    
    def get_status(self):
        return Status(self.status).name
    
    def reset(self):
        self.status = Status.PENDING.value
        self.save()
    
    def accept(self):
        self.status = Status.APPROVED.value
        self.save()

    def reject(self):
        self.status = Status.REJECTED.value
        self.save()
    
    def confirm(self):
        self.status = Status.CONFIRMED.value
        self.save()
                                
