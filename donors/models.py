from django.db import models
from django.contrib.auth.models import User
from .constants import BLOOD_GROUPS

class DonorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    phone = models.CharField(max_length=15)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"

class BloodRequest(models.Model):
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, blank=True, null=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_sent")
    donors = models.ManyToManyField(User, related_name="requests_received") 
    accepted_donors = models.ManyToManyField(User, related_name="accepted_requests", blank=True)
    accepted_count = models.IntegerField(default=0)  # Track accepted donors
    request_ignored_by_donors = models.ManyToManyField(User, related_name="ignored_donors", blank=True)
    rejected_donors_by_requester = models.ManyToManyField(User, related_name="rejected_donor_request", blank=True)
    final_donors = models.ManyToManyField(User, related_name="final_donors", blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    total_accepted = models.IntegerField(null=True, blank=True, default=0)
    detail_address = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.requester.username} requested for {self.blood_group} Blood"

class DonationHistory(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_donations")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.username} donated to {self.receiver.username}"
    
class HelpRequester(models.Model):
    blood_request_id = models.IntegerField(10, blank=True, null=True)
    helper = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name="helper", null=True, blank=True)
    requester = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name="requester", null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.requester.user.username} - {self.blood_group} Blood Request and Helper {self.name} - {self.helper.user.username}"
    
    
    
class CustomBloodRequest(models.Model):
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, blank=True, null=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="custom_requests_sent")
    donors = models.ManyToManyField(User, related_name="custom_requests_received")
    accepted_donors = models.ManyToManyField(User, related_name="accepted_custom_requests", blank=True)
    accepted_count = models.IntegerField(default=0)
    request_ignored_by_donors = models.ManyToManyField(User, related_name="ignored_custom_donors", blank=True)
    rejected_donors_by_requester = models.ManyToManyField(User, related_name="rejected_custom_donor_request", blank=True)
    final_donors = models.ManyToManyField(User, related_name="custom_final_donors", blank=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    total_accepted = models.IntegerField(null=True, blank=True, default=0)
    detail_address = models.CharField(max_length=100, null=True, blank=True)
    
    contact_number = models.IntegerField()
    note = models.TextField(null=True, blank=True)
    donation_date = models.DateField(null=True, blank=True)
    donation_time = models.TimeField(null=True, blank=True)
    receiver_latitude = models.FloatField(null=True, blank=True)
    receiver_longitude = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.requester.username} requested for {self.blood_group} Blood"
