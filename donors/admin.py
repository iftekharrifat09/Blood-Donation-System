from django.contrib import admin
from .models import DonorProfile, BloodRequest
# Register your models here.


admin.site.register(DonorProfile)
admin.site.register(BloodRequest)
