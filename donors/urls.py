from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.user_signup, name="signup"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("update-location/", views.update_location, name="update_location"),
    path("search-blood/", views.search_blood, name="search_blood"),
    path("send-request/", views.send_request, name="send_request"),
    path("accept-blood-request/<int:request_id>", views.accept_blood_request, name="accept_blood_request"),
    path("ignore-blood-request/<int:request_id>", views.ignore_blood_request, name="ignore_blood_request"),
    path("approve-blood-request/<int:request_id>/<int:donor_id>", views.approve_blood_request, name="approve_blood_request"),
    path("reject-donor-request/<int:request_id>/<int:donor_id>", views.reject_donor_request, name="reject_donor_request"),
    
]
