from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from newsapp.models import UserProfile
from newsapp.forms import UserProfileForm
# Create your views here.
# @login_required(login_url='login')


def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

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
    user_profile, created = UserProfile.objects.get_or_create(
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
