from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from .constants import BLOOD_GROUPS, GENDER_CHOICE
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE)
    age =  models.IntegerField(default=18)
    profession = models.CharField(max_length=50)
    profession_institute_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    
    phone_number = PhoneNumberField(unique=True, verbose_name="Phone number", region="BD", blank=True, null=True)  # Default region Bangladesh
    national_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return f'Profile of {self.user.username}'
