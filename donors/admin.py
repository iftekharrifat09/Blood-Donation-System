from django.contrib import admin
from .models import DonorProfile, BloodRequest, DonationHistory, HelpRequester
# Register your models here.


admin.site.register(DonorProfile)
admin.site.register(BloodRequest)
admin.site.register(DonationHistory)
admin.site.register(HelpRequester)
