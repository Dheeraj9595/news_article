from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse, redirect, render

from newsapp.forms import UserProfileForm
from newsapp.models import UserProfile


def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check if the passwords match
        if pass1 != pass2:
            messages.error(
                request, 'Your password and confirm password are not the same.')
            # Assuming 'signup' is the name of the signup view
            return redirect('signup')
        else:
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                messages.info(
                    request, f'Successfully registered {uname}! Please log in.')
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'Username already exists.')
                # Assuming 'signup' is the name of the signup view
                return redirect('signup')
    # Assuming you have a signup.html template for GET requests.
    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('headlines')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')

# ---------------profile--------------------------------------------------


@login_required
def user_profile(request):
    user_profile = UserProfile.objects.get_or_create(
        user=request.user)

    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)


@login_required
def edit_user_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user)

    if request.method == "POST":
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            # Redirect to the user's profile after successful edit
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form
    }
    return render(request, 'edit_profile.html', context)
