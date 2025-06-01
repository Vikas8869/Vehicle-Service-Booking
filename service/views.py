from django.shortcuts import render,redirect
from .models import *

# Create your views here.

def index(request):
    return render(request,"index.html")

def home_page(request):
    return render(request,"home_page.html")
def aboutus(request):
    return render(request,"aboutus.html")
def contact_page(request):
    return render(request,"contact_page.html")
def charges(request):
    return render(request,"charges.html")


def service_page(request):
    if request.method=="POST":
        data=request.POST
        owner_name=data.get('owner_name')
        email=data.get('email')
        phone=data.get('phone')
        vehicle_no=data.get('vehicle_no')
        trip=data.get('trip')
        address=data.get('address')
        last_service=data.get('last_service')
        booking_date=data.get('booking_date')
        problems=data.get('problems')

        Service.objects.create(
            owner_name=owner_name,
            email=email,
            phone=phone,
            vehicle_no=vehicle_no,
            trip=trip,
            address=address,
            last_service=last_service,
            booking_date=booking_date,
            problems=problems,
        )
        return redirect('/service_page/')
    return render(request,"service_page.html")
def service_view(request):
    queryset=Service.objects.all()
    context={'data':queryset}
    return render(request,"service_view.html",context)

def service_update(request, id):
    queryset = Service.objects.get(id=id)
    
    if request.method == "POST":
        data = request.POST
        queryset.owner_name = data.get('owner_name')
        queryset.email = data.get('email')
        queryset.phone = data.get('phone')
        queryset.vehicle_no = data.get('vehicle_no')
        queryset.trip = data.get('trip')
        queryset.address = data.get('address')
        queryset.last_service = data.get('last_service')
        queryset.booking_date = data.get('booking_date')
        queryset.problems = data.get('problems')
        # ✅ Save the updated data
        queryset.save()
        # Optional: Redirect to some page after saving
        return redirect('service_view')  # Replace with your success page name

    context = {'data': queryset}
    return render(request, "service_update.html", context)

def cancel_service(request,id):
    queryset=Service.objects.get(id=id)
    queryset.delete()
    return redirect('service_view')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
# from .forms import LoginForm, SignupForm, ForgotPasswordForm, OTPVerificationForm, ResetPasswordForm
from .models import OTP, generate_otp
from django.utils import timezone
from datetime import timedelta

def login_view(request):
    if request.user.is_authenticated:
        return redirect('service_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('service_page')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')

    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home_page')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            OTP.objects.filter(user=user).delete()
            OTP.objects.create(user=user, otp=otp, created_at=timezone.now())
            send_otp_email(request, email, otp)
            request.session['forgot_user_id'] = user.id
            messages.success(request, f'OTP sent to {email}')
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')

    return render(request, 'forgot_password.html')

def verify_otp_view(request):
    user_id = request.session.get('forgot_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Try again.')
        return redirect('forgot_password')

    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        try:
            otp_obj = OTP.objects.get(user_id=user_id, otp=otp_input)
            if timezone.now() - otp_obj.created_at > timedelta(minutes=5):
                otp_obj.delete()
                messages.error(request, 'OTP expired.')
            else:
                request.session['reset_permission'] = True
                return redirect('reset_password')
        except OTP.DoesNotExist:
            messages.error(request, 'Invalid OTP.')

    return render(request, 'verify_otp.html')

# Reset password
def reset_password_view(request):
    user_id = request.session.get('forgot_user_id')
    if not request.session.get('reset_permission') or not user_id:
        messages.error(request, 'Unauthorized access.')
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        else:
            user = User.objects.get(id=user_id)
            user.set_password(new_password)
            user.save()
            OTP.objects.filter(user=user).delete()
            del request.session['forgot_user_id']
            del request.session['reset_permission']
            messages.success(request, 'Password reset successful.')
            return redirect('login')

    return render(request, 'reset_password.html')

# Send OTP via email
def send_otp_email(request, email, otp):
    subject = "Your OTP for Password Reset"
    message = f"Your OTP is: {otp}. It expires in 5 minutes."
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])