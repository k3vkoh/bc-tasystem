from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    eagleid = models.PositiveIntegerField(default=0000000)
    professor = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    courses = models.ManyToManyField("courses.Course", blank=True)
    course_working_for = models.ForeignKey(
        "courses.Course", on_delete=models.CASCADE, null=True, blank=True, related_name='course_working_for')
    applications = models.ManyToManyField(
        "applications.Application", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def is_professor(self):
        return self.professor

    def is_student(self):
        return not self.professor

    def reached_max_applications(self):
        return self.applications.count() >= 5

    def already_applied_to_course(self, course):
        return self.applications.filter(course=course).exists()

    def is_ta(self):
        return self.course_working_for is not None
