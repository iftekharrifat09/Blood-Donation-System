from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from . import models
from .constants import BLOOD_GROUPS, GENDER_CHOICE

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    gender = forms.ChoiceField(choices=GENDER_CHOICE, required=True)
    age = forms.IntegerField()
    profession = forms.CharField(max_length=50, required=True) 
    profession_institute_name = forms.CharField(max_length=100, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS, required=True)
    
    phone_number = PhoneNumberField(required=True, region="BD", widget=forms.TextInput(attrs={'class': 'phone-input'}))
    national_id = forms.CharField(max_length=20, required=True)
    profile_picture = forms.ImageField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'gender', 'age', 'profession', 'profession_institute_name', 'address','blood_group', 'phone_number', 'national_id', 'profile_picture']  
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different one.")
        return email
    
    # def clean_phone_number(self):
    #     phone_number = self.cleaned_data.get('phone_number')
    #     if len(phone_number) != 13:  # Ensure exactly 11 digits
    #         raise forms.ValidationError("Phone number must be (11 digits)")
    #     return phone_number
    
    def save(self, commit = True):
        user = super().save(commit=False)
        if commit:
            user.save()
            models.UserProfile.objects.create(
                user = user,
                gender = self.cleaned_data['gender'],
                age = self.cleaned_data['age'],
                profession = self.cleaned_data['profession'],
                profession_institute_name = self.cleaned_data['profession_institute_name'],
                address = self.cleaned_data['address'],
                blood_group = self.cleaned_data['blood_group'],
                phone_number = self.cleaned_data['phone_number'],
                national_id = self.cleaned_data['national_id'],
                profile_picture = self.cleaned_data['profile_picture'],
            )
        return user