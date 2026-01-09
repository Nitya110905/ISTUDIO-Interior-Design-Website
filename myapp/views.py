from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from django.conf import settings
from django.core.mail import send_mail
import random
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
            subject = 'OTP for Forgot-Password!'
            otp = random.randint(111111,999999)
            msg = 'Hi ' + user.name + ', Your OTP is : ' + str(otp) + '.' 
            email_from = settings.EMAIL_HOST_USER
            recepient_list = [user.email]
            send_mail(subject,msg,email_from,recepient_list)
            request.session['email'] = user.email
            request.session['otp'] = otp
            messages.success(request,'OTP sent successfully !')
            return redirect ('otp')
        except User.DoesNotExist:
            messages.error(request,'Email does not exist!')
            return render(request,'forgot-password.html')
    else:
        return render(request,'forgot-password.html')


def otp(request):
    try:
        otp = int(request.session['otp'])
        uotp = int(request.POST['uotp'])
        
        if otp == uotp:
            del request.session['otp']
            return redirect('newpass')
        else:
            messages.error(request,'Invalid OTP !')
            return render(request,'otp.html')
    except Exception as e:
        print("Exception : ",e)
        return render(request,'otp.html')

def femail(request):
    return render(request,'forgot-email.html')

def newpass(request):
    return render(request,'new-password.html')
            

