from django.db import models
from users.models import CustomUser
from django.urls import reverse
from django.db.models import Q
import uuid


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    term = models.CharField(max_length=100)
    class_type = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    course_title = models.CharField(max_length=100)
    instructor_first_name = models.CharField(max_length=100)
    instructor_last_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    timeslot = models.CharField(max_length=100)
    max_enroll = models.IntegerField()
    room_size = models.IntegerField()
    num_tas = models.IntegerField()
    description = models.CharField(max_length=350, null=True, blank=True)
    status = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    professor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='courses', null=True, blank=True)

    current_tas = models.ManyToManyField(
        CustomUser, related_name='course_working_for', blank=True)

    has_discussions = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course_title} ({self.section}) - {self.class_type}"

    def get_absolute_url(self):
        return reverse('home')

    def get_object(self):
        return self