from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .tokens import generate_token

from .util import send_welcome_email, send_activation_email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, smart_str
from django.contrib.auth.decorators import login_required

# Create your views here.


# @login_required(login_url="/signin/")
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

        elif User.objects.filter(username=email).exists():
            error_message = "Email already exists. Please choose a different email."

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
            user.is_active = False

            messages.success(request, 'Registration successful. You can now log in.')
            # Send Welcome message
            welcome_message = f"Dear {user.username},\n\nThank you for signing up on our website. We are excited to " \
                              f"have you on board!\n\nTo activate your account, please check your email for the next " \
                              f"message.\n\nOnce your account is activated, you can log in using your " \
                              f"credentials.\n\nIf you have any questions or need assistance, please feel free to " \
                              f"contact us.\n\nBest regards,\nThe Team"

            send_welcome_email(
                from_email=settings.EMAIL_HOST,
                user_email=user.email,
                subject='Wellcome to our website',
                message=welcome_message
            )

            # Send activation message
            token = generate_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk)),
            send_activation_email(request=request, email=user.email, username=user.username, uid=uid, token=token)
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
            messages.success(request, f'Login successful with username {user.username}.')
            return redirect('authentication:home')
        else:
            # Invalid username or password, display error message
            error_message = "Invalid username or password. Please try again."
            messages.warning(request, error_message)
    return render(request, 'authentication/signin.html')


def sign_out(request):
    # Log out the user
    logout(request)
    messages.success(request, 'You have been successfully signed out.')
    return redirect('authentication:home')


def activate(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(smart_str(uidb64 + '==')))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('authentication:home')
    else:
        return render(request, 'authentication/activate_fail.html')


