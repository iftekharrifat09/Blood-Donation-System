from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from .models import DonorProfile, BloodRequest, DonationHistory, HelpRequester, CustomBloodRequest
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from math import radians, cos, sin, sqrt, atan2, asin
from datetime import datetime
from django.db.models import Q
from collections import defaultdict

def home_page(request):
    return render(request, "home_page.html")

def user_signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to login page after registration
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form, 'type':'signup'})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login Successful")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
    else:
        form = AuthenticationForm()
    return render(request, 'register.html', {'form': form, 'type':'login'})


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect('login')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    my_requests_for_blood = BloodRequest.objects.filter(requester=request.user).order_by("-created_at")
    active_requests_myGroup = BloodRequest.objects.filter(blood_group=request.user.donorprofile.blood_group, donors__in=[request.user]).exclude(requester=request.user).order_by("-created_at")
    #, accepted_donors__in=[request.user] 
    active_requests_otherGroup = BloodRequest.objects.filter(status="Pending").exclude(Q(requester=request.user) | Q(blood_group=request.user.donorprofile.blood_group)).order_by("-created_at")
    requester_id =  request.user.id
    requester = get_object_or_404(DonorProfile, user_id=requester_id)
    print(requester)
    help_post = HelpRequester.objects.filter(requester = requester).order_by("-created_at")
    
    if help_post:
        for post in help_post:
            print(post.id)
    else:
        print("No help post found")
         
    context = {
        "my_requests_for_blood": my_requests_for_blood,
        "active_requests_myGroup": active_requests_myGroup,
        "active_requests_otherGroup": active_requests_otherGroup, 
        "help_post": help_post,
    }
    return render(request, "dashboard.html", context)



@login_required
def update_location(request):
    if request.method == "POST":
        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")
        if lat and lon:
            profile = DonorProfile.objects.get(user=request.user)
            profile.latitude = lat
            profile.longitude = lon
            profile.save()
            return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})

@login_required
def search_blood(request):
    user_profile = request.user.donorprofile
    user_lat, user_lng = user_profile.latitude, user_profile.longitude
    # Get all pending blood requests (always load these)
    # Get all available donors (always load these)
    filtered_donors = []
    
    if request.method == "POST":
        blood_group = request.POST.get("blood_group")
        radius_km = float(request.POST.get("radius"))
        detail_address = request.POST.get("detail_address")
        description = request.POST.get("description")
        

        # Function to calculate distance
        def calculate_distance(lat1, lon1, lat2, lon2):
            R = 6371  # Radius of the Earth in km
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            return R * c  # Distance in km

        # Get all donors with the requested blood group
        all_donors = DonorProfile.objects.filter(blood_group=blood_group).exclude(user=request.user)
        
        # Filter donors within the radius
        donors = [donor for donor in all_donors if calculate_distance(user_lat, user_lng, donor.latitude, donor.longitude) <= radius_km]
        filtered_donors = donors
        
        for donor in filtered_donors:
            print(donor.user.username)
        
        if donors: 
            blood_request = BloodRequest.objects.create( # Create a new blood request only if there are donors
                blood_group=blood_group,
                requester=request.user, 
                status="Pending",
                detail_address = detail_address,
                description=description,
            )
            # if created:  # Only add donors if a new request was created
            #     blood_request.donors.add(*[donor.user for donor in donors])

            # Add all donors to this request
            blood_request.donors.add(*[donor.user for donor in donors])
        # return redirect(reverse("search_blood"))
        
    
    return render(request, "search_blood.html", {"donors": filtered_donors})


@login_required
def send_request(request):
    if request.method == "POST":
        donor_id = request.POST.get("donor_id")
        donor = User.objects.get(id=donor_id)
        # Check if the current user (receiver) has already requested blood from this donor
        existing_request = BloodRequest.objects.filter(requester=request.user, donor=donor).exists()

        if existing_request:
            messages.error(request, "You have already sent a request to this donor.")
            return redirect("search_blood")  # Redirect to a relevant page

        BloodRequest.objects.create(requester=request.user, donor=donor, status="Pending")

        # Send Email Notification
        send_mail(
            "Blood Donation Request",
            f"Dear {donor.username}, you have a new blood donation request from {request.user.username}.",
            "noreply@blooddonation.com",
            [donor.email],
            fail_silently=False,
        )

        return JsonResponse({"message": "Request sent successfully!"})
    
    

@login_required
def accept_blood_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    # Check if the request is already accepted by 2 donors
    if blood_request.accepted_count >= 2:
        messages.error(request, "This blood request is already fulfilled.")
        return redirect("dashboard")  # Redirect to donor's dashboard

    # Ensure donor is in the request's donor list
    if request.user not in blood_request.donors.all():
        messages.error(request, "You are not eligible to accept this request.")
        return redirect("dashboard")

    # Ensure donor hasn't already accepted
    if request.user in blood_request.request_ignored_by_donors.all():
        messages.error(request, "You have already Ignored this request.")
        return redirect("dashboard")
    
    if request.user in blood_request.accepted_donors.all():
        messages.error(request, "You have already accepted this request.")
        return redirect("dashboard")

    # Accept request
    blood_request.accepted_donors.add(request.user)
    blood_request.accepted_count += 1
    blood_request.save()

    # If 2 donors have accepted, remove from others' profiles
    if blood_request.accepted_count >= 2:
        blood_request.status = "Fulfilled"
        blood_request.save()

    messages.success(request, "You have successfully accepted the request.")
    return redirect("dashboard")  # Redirect after acceptance


def ignore_blood_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    # Ensure donor hasn't already accepted
    if request.user in blood_request.request_ignored_by_donors.all():
        messages.error(request, "You have already Ignored this request.")
        return redirect("dashboard")
    
    if request.user in blood_request.accepted_donors.all() and request.user not in blood_request.rejected_donors_by_requester.all():
        messages.error(request, "You have already accepted this request.")
        return redirect("dashboard")
    
    blood_request.request_ignored_by_donors.add(request.user)
    messages.success(request, "You have Ignored the request.")

    return redirect("dashboard")  # Redirect back to search page


def approve_blood_request(request, request_id, donor_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    donor = User.objects.get(id=donor_id)
    
    if request.user in blood_request.final_donors.all():
        messages.error(request, "You have already Select for blood donation for the blood request.")
    elif donor in blood_request.final_donors.all():
        messages.error(request, "This donor has already selected for blood donation for the blood request.")
    elif donor in blood_request.rejected_donors_by_requester.all():
        messages.error(request, "This donor has rejected by the requester for the blood request.")
    else:
        blood_request.final_donors.add(donor)
        messages.success(request, "You are Select for Blood donation, Please contact with the receiver for more information.")
        DonationHistory.objects.create(donor=donor, receiver = request.user)

    return redirect("dashboard")  # Redirect back to search page

def reject_donor_request(request, request_id, donor_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    donor = User.objects.get(id=donor_id)
    
    if request.user in blood_request.rejected_donors_by_requester.all():
        messages.error(request, "You have rejected by the requester for this blood donation request")
    elif donor in blood_request.final_donors.all():
        messages.error(request, "This donor has already selected for blood donation for the blood request.")
    elif donor in blood_request.rejected_donors_by_requester.all():
        messages.error(request, "This donor has rejected by the requester for the blood request.")
    else:
        blood_request.rejected_donors_by_requester.add(donor)
        messages.success(request, "You are reject by the requester for this blood donation request")

    return redirect("dashboard")  # Redirect back to search page

def delete_blood_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    
    if request.user == blood_request.requester:
        blood_request.delete()
        messages.success(request, "Blood Request deleted successfully.")
        return redirect("dashboard") 
    else:
        messages.error(request, "You are not authorized to delete this blood request.")
        return redirect("dashboard")


def help_form(request, sender_id, requester_id, request_id):
    
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        
        sender = get_object_or_404(DonorProfile, user_id=sender_id)
        requester = get_object_or_404(DonorProfile, id=requester_id)
        print(sender, requester)
        print(name, phone, message, sender_id, requester_id, request_id,  sender.blood_group)
        
        print(DonorProfile.objects.filter(id=sender_id).exists())  # Check if sender exists
        print(DonorProfile.objects.filter(id=requester_id).exists())  
        # You can process and save the data here if needed
        # Save the help request
        HelpRequester.objects.create(
            blood_request_id=request_id,
            helper=sender,
            requester=requester,
            blood_group=sender.blood_group,
            name=name,
            phone=phone,
            message=message,
        )

    return redirect('dashboard')  # Redirect back to the dashboard




def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # haversine formula 
    dlat = lat2 - lat1 
    dlon = lon2 - lon1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Radius of earth in kilometers
    return c * r

@login_required
def create_blood_request(request):
    donors = DonorProfile.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)

    if request.method == "POST":
        lat = float(request.POST.get("patient_latitude", 0))
        lng = float(request.POST.get("patient_longitude", 0))
        radius_str = request.POST.get("the_radius", "").strip()
        radius = float(radius_str) if radius_str else 1.0  # Safe default
        blood_group = request.POST.get("blood_group")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        donation_note = request.POST.get("donation_note")
        donation_date = request.POST.get("donation_date")
        donation_time = request.POST.get("donation_time")

        filtered_donors = []
        for donor in donors.filter(blood_group=blood_group):
            if donor.latitude and donor.longitude:
                distance = haversine(lat, lng, donor.latitude, donor.longitude)
                if distance <= radius:
                    filtered_donors.append(donor)

        if not filtered_donors:
            messages.error(request, "No donor found within the selected radius.")
            return render(request, "custom_blood_request.html", {"donors": donors})

        messages.success(request, f"Donor found: {len(filtered_donors)}")

        created_donor_names = []

        for donor in filtered_donors:
            # Check if a request already exists for this donor
            existing = CustomBloodRequest.objects.filter(
                requester=request.user,
                donors=donor.user,
                blood_group=blood_group,
                receiver_latitude=lat,
                receiver_longitude=lng
                
            ).first()

            if not existing:
                request_entry = CustomBloodRequest.objects.create(
                    blood_group=blood_group,
                    requester=request.user,
                    detail_address=address,
                    contact_number=contact,
                    note=donation_note,
                    donation_date=donation_date or None,
                    donation_time=donation_time or None,
                    receiver_latitude=lat,
                    receiver_longitude=lng,
                    created_at=datetime.now()
                )
                request_entry.donors.add(donor.user)
                created_donor_names.append(donor.user.username)

        if created_donor_names:
            donor_list_str = ", ".join(created_donor_names)
            messages.success(request, f"Request sent successfully to: {donor_list_str}")
        else:
            messages.info(request, "All selected donors have already received the request.")

        return render(request, "custom_blood_request.html", {
            "donors": filtered_donors
        })

    return render(request, "custom_blood_request.html", {
        "donors": donors
    })

