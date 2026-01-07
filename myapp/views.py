from django.shortcuts import render
from .models import User

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

def SignUp(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            msg = "User already exists!!"
            return render(request,'Sign-Up.html',{'msg':msg})
        except User.DoesNotExist:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    password = request.POST['password'],
                    contact = request.POST['contact']
                )
                msg = "Sign-Up Successfull !!!"
                return render (request,'Login.html',{'msg':msg})
            else:
                msg = "Password and Confirm Password does not match !!!"
                return render (request,'Sign-Up.html',{'msg':msg})
    else:
        return render (request,'Sign-Up.html')
    

def Login(request):
    return render(request,'Login.html')
            

