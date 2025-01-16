from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.urls import reverse
from allauth.account.utils import send_email_confirmation

from . import forms

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    context = {"profile": profile}
    return render(request, "users/profile.html", context=context)


@login_required
def profile_edit_view(request):
    form = forms.ProfileForm(instance=request.user.profile)  
    
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
        
    if request.path == reverse("users:profile-onboarding"):
        onboarding = True
    else:
        onboarding = False
    context = {"form": form, "onboarding": onboarding}
      
    return render(request, "users/profile_edit.html", context=context)


@login_required
def profile_settings_view(request):
    return render(request, "users/profile_settings.html")


@login_required
def profile_emailchange(request):
    
    if request.htmx:
        form = forms.EmailForm(instance=request.user)
        context = {'form':form}
        return render(request, "partials/email_form.html", context=context)
    
    if request.method == 'POST':
        form = forms.EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            
            # Check if the email already exists
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f"{email} is already in use.")
                return redirect("users:profile-settings")
            
            form.save() 
            
            # Then Signal updates emailaddress and set verified to False
            
            # Then send confirmation email 
            send_email_confirmation(request, request.user)
            
            return redirect("users:profile-settings")
        else:
            messages.warning(request, "Form not valid")
            return redirect("users:profile-settings")
        
    return redirect("home:home-index")


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect("users:profile-settings")


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Account deleted, what a pity")
        return redirect("home:home-index")
    
    return render(request, "users/profile_delete.html")