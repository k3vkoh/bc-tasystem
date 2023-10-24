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
    course_working_for = models.ForeignKey("courses.Course", on_delete=models.CASCADE, null=True, blank=True, related_name='course_working_for')
    applications = models.ManyToManyField("applications.Application", blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # def save(self, *args, **kwargs):
    #     self.professor = self.is_professor()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def is_professor(self):
        professor_list_short = [
            'alvarez@bc.edu',
            'aviram@bc.edu',
            'bentoayr@bc.edu',
            'bers@bc.edu',
            'biswasaa@bc.edu',
            'bolotinn@bc.edu',
            'creiner@bc.edu',
            'griff@bc.edu',
            'guptanq@bc.edu',
            'kimry@bc.edu',
            'levear@bc.edu',
            'marquemo@bc.edu',
            'mctaguec@bc.edu',
            'mohlerg@bc.edu',
            'prudhome@bc.edu',
            'straubin@bc.edu',
            'suhx@bc.edu',
            'volkovic@bc.edu',
            'weidf@bc.edu',
            'wisemacc@bc.edu',
            'yunmd@bc.edu',
        ]

        professor_list_long = [
            'sergio.alvarez@bc.edu',
            'amittai.aviram@bc.edu',
            'jose.bento@bc.edu',
            'marina.bers@bc.edu',
            'anjum.biswas@bc.edu',
            'naomi.bolotin@bc.edu',
            'alexander.creiner@bc.edu',
            'william.griffith@bc.edu',
            'nikhil.gupta.3@bc.edu',
            'nam.wook.kim@bc.edu',
            'duncan.levear@bc.edu',
            'maira.marquessamary@bc.edu ',
            'carl.mctague@bc.edu',
            'george.mohler@bc.edu',
            'emily.prudhommeaux.1@bc.edu',
            'howard.straubing@bc.edu',
            'hsinhao.su@bc.edu',
            'ilya.volkovich@bc.edu',
            'donglai.wei@bc.edu',
            'charles.wiseman@bc.edu',
            'mira.yun@bc.edu',
        ]
        return self.email in professor_list_long or self.email in professor_list_short
    
    
    def is_student(self):
        return not self.professor and not self.is_superuser

    def reached_max_applications(self):
        return self.applications.count() >= 5

    def already_applied_to_course(self, course):
        return self.applications.filter(course=course).exists()
    
    def is_ta(self):
        return self.course_working_for is not None


    
