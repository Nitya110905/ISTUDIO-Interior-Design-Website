from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from django.conf import settings
from django.core.mail import send_mail
import random
import time
# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def feature(request):
    return render(request,'feature.html')

def project(request):
    return render(request,'project.html')

def service(request):
    return render(request,'service.html')

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')

def signup(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            messages.error(request,"User already exists !")
            return render(request,'sign-up.html')
        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    contact = request.POST['contact']
                )
                messages.success(request, "sign-up Successful !")
                return redirect ('login')
            else:
                messages.error(request, "Password and Confirm Password do not match !")
                return render(request, 'sign-up.html')
    else:
        return render (request,'sign-up.html')
    

def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                messages.success(request,"Login Successful !")
                return redirect('index')
            else:
                messages.error(request, "Incorrect Credentials !")
                return render (request,'login.html')
        except User.DoesNotExist:
            messages.error(request,"Incorrect Credentials !")
            return render(request,'login.html')
    else:
        return render (request,'login.html')

def logout(request):
    del request.session['email']
    return redirect('login')

def fpass(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email = request.POST['email'])
            subject = 'OTP for Forgotten-Password !'
            otp = random.randint(111111,999999)
            msg = 'Hi ' + user.name + ', Your OTP is : ' + str(otp) + '.' 
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [user.email]
            send_mail(subject,msg,email_from,recepient_list)

            request.session['resetpass_email'] = user.email
            request.session['otp'] = otp
            request.session['otp_timestamp'] = time.time()

            messages.success(request,'OTP sent successfully !')
            return redirect ('otp')
        except User.DoesNotExist:
            messages.error(request,'Email does not exist !')
            return render(request,'forgot-password.html')
    else:
        return render(request,'forgot-password.html')


def otp(request):

    if 'resetpass_email' not in request.session:
        messages.error(request, "Please enter your email first !")
        return redirect('fpass')
    
    created_time = request.session.get('otp_timestamp', 0)
    current_time = time.time()
    elapsed_time = int(current_time - created_time)
    seconds_left = max(0, 60 - elapsed_time) # max(0, ...) is a cleaner way to ensure it's not negative

    if request.method == "POST":
        try:
            saved_otp = request.session.get('otp')
            user_otp = request.POST.get('uotp') 

            if seconds_left <= 0:
                messages.error(request, "OTP Expired !")
                return render(request, 'otp.html', {'seconds_left': 0}) 
            
            if saved_otp and user_otp and int(saved_otp) == int(user_otp):
                del request.session['otp'] 
                messages.success(request, "OTP Verified!")
                return redirect('newpass')
            
            else:
                messages.error(request, 'Invalid OTP !')
                return render(request, 'otp.html', {'seconds_left': seconds_left})
        
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid number !')
            return render(request, 'otp.html', {'seconds_left': seconds_left})

    return render(request, 'otp.html', {'seconds_left': seconds_left})

def resend_otp(request):
    if 'resetpass_email' not in request.session:
        messages.error(request, "Please enter your email first !")
        return redirect('fpass')
    
    email = request.session.get('resetpass_email')
    
    if email:
        try:
            user = User.objects.get(email=email)
            new_otp = random.randint(111111, 999999)
            request.session['otp'] = new_otp
            request.session['otp_timestamp'] = time.time() # Resets the 60s timer

            subject = 'New OTP for Forgotten-Password!'
            msg = f'Hi {user.name}, Your NEW OTP is : {new_otp}.'
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, msg, email_from, [user.email])
            
            messages.success(request, "A new OTP has been sent !")
            return redirect('otp')
            
        except User.DoesNotExist:
            messages.error(request, "User account error !")
            return redirect('fpass')
    else:
        messages.error(request, "Session expired. Please enter your email again !")
        return redirect('fpass')

def femail(request):
    return render(request,'forgot-email.html')

def newpass(request):
    if 'resetpass_email' not in request.session:
        messages.error(request, "Please enter your email first !")
        return redirect('fpass')
    
            

