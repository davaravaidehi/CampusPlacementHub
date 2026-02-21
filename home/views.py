from django.shortcuts import render, HttpResponse

def index(request):
    context = {
        'variable' : "THIS IS SEDS"
    }
    return render(request,'index.html',context)
    # return HttpResponse("This is home page.")
def about(request):
    return HttpResponse("This is about page.")
def services(request):
    return HttpResponse("This is service page.")
def contact(request):
    return HttpResponse("This is contact page.")
def student_login(request):
    return render(request,'student_login.html')
def placement_login(request):
    return render(request,'placement_login.html')
def student_signup(request):
    return render(request,'student_signup.html')
def forgot_password(request):
    return render(request,'forgot_password.html')

def university_dashboard(request):
    return render(request,'university_dashboard.html')
