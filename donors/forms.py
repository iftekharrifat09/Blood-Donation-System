from django import forms
from django.contrib.auth.models import User
from .models import DonorProfile
from .constants import BLOOD_GROUPS

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    blood_group = forms.ChoiceField(choices=BLOOD_GROUPS)
    phone = forms.CharField(max_length=15)
    latitude = forms.FloatField(required=False)  # Allow optional
    longitude = forms.FloatField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "blood_group", "phone"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash password
        if commit:
            user.save()
            DonorProfile.objects.create(
                user=user,
                blood_group=self.cleaned_data["blood_group"],
                phone=self.cleaned_data["phone"],
                latitude=self.cleaned_data.get("latitude", None),
                longitude=self.cleaned_data.get("longitude", None),
            )
        return user