from django.db import models
from users.models import CustomUser as User
from courses.models import Course
from enum import Enum
from django.urls import reverse
import uuid


class ApplicationStatus(Enum):
    '''
    Enum for the status of an application
    PENDING - The application has been submitted but not yet reviewed
    APPROVED - The application has been accepted by the professor
    REJECTED - The application has been rejected by the professor or the offer has been rejected by the student
    CONFIRMED - The application offer has been confirmed by the student
    '''
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
    CONFIRMED = 4


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, related_name='applications')

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, default=None, related_name='applications')

    additional_information = models.TextField(max_length=500, blank=True)

    status = models.IntegerField(choices=[(
        tag.value, tag.name) for tag in ApplicationStatus], default=ApplicationStatus.PENDING.value)

    def __str__(self):
        return self.student.first_name + ' ' + self.student.last_name + ' - ' + self.course.course_title

    def get_absolute_url(self):
        return reverse('applications:application-detail', kwargs={'pk': self.pk})

    def get_status(self):
        return ApplicationStatus(self.status).name

    def reset(self):
        self.status = ApplicationStatus.PENDING.value
        self.save()

    def accept(self):
        self.status = ApplicationStatus.ACCEPTED.value
        self.save()

    def reject(self):
        self.status = ApplicationStatus.REJECTED.value
        self.save()

    def confirm(self):
        self.status = ApplicationStatus.CONFIRMED.value
        self.save()
