from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    STUDENT = 'STUDENT'
    PSYCHOLOGIST = 'PSYCHOLOGIST'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (PSYCHOLOGIST, 'Psychologist'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')])
    career = models.CharField(max_length=255)

    def __str__(self):
        return f"Profile of {self.user.email}"