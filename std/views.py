from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Student

def home(request):
    std=Student.objects.all()
    return render(request,"std/home.html", {'std':std})

def std_app(request):
    if request.method == 'POST':
        print("Added")
        #retrive the user inputs
        stds_roll=request.POST.get("std_roll")
        stds_name=request.POST.get("std_name")
        stds_email=request.POST.get("std_email")
        stds_phone=request.POST.get("std_phone")
        stds_address=request.POST.get("std_address")
        stds_department=request.POST.get("std_department")
        stds_course=request.POST.get("std_course")
        stds_password=request.POST.get("std_password")

        #create an object for models:
        s=Student()
        s.roll=stds_roll
        s.name=stds_name
        s.email=stds_email
        s.phone=stds_phone
        s.address=stds_address
        s.department=stds_department
        s.course=stds_course
        s.password=stds_password
        s.save()
        return redirect("/std/home")
    
    return render(request,"std/add_std.html",{})

def delete_std(request, roll):
    student = Student.objects.get(pk=roll)
    student.delete()
    return redirect("/std/home")

def update_std(request,roll):
    std = Student.objects.get(pk=roll)
    return render(request,"std/update_std.html",{'std':std})

def do_update_std(request,roll):
    std_roll=request.POST.get("std_roll")
    std_name=request.POST.get("std_name")
    std_email=request.POST.get("std_email")
    std_phone=request.POST.get("std_phone")
    std_address=request.POST.get("std_address")
    std_department=request.POST.get("std_department")
    std_course=request.POST.get("std_course")
    std_password=request.POST.get("std_password")

    std = Student.objects.get(pk=roll)
    std.roll=std_roll
    std.name=std_name
    std.email=std_email
    std.phone=std_phone
    std.address=std_address
    std.department=std_department
    std.course=std_course
    std.password=std_password
    std.save()
    return redirect("/std/home/")


