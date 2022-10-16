from django.shortcuts import render
from .models import Dashboard
from account.models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    user = request.user
    user_dashboard = Dashboard.objects.get(user=user)
    profile_name = Profile.objects.get(user=user)
    referral = "http://127.0.0.1:8000/account/ref/"+str(profile_name.profile_name)
    return render(request,"dashboard/dash.html",{"user_dashboard":user_dashboard,"referral":referral})