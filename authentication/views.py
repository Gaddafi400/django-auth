from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login


# Create your views here.


def home(request):
    return render(request, template_name="authentication/index.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmpassword')

        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
        elif password != confirm_password:
            error_message = "Passwords do not match. Please try again."
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=firstname,
                last_name=lastname
            )
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('authentication:home')

        messages.warning(request, error_message)
        return render(request, 'authentication/signup.html', {'error_message': error_message})
    return render(request, 'authentication/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            # Authentication successful, log in the user
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('authentication:home')
        else:
            # Invalid username or password, display error message
            error_message = "Invalid username or password. Please try again."
            messages.info(request, error_message)
    return render(request, 'authentication/signin.html')


def sign_out(request):
    return render(request, template_name="authentication/sign_out.html")
