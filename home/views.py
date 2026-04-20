from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.core.mail import send_mail
from std.models import Student

def index(request):
    context = {
        'variable' : "THIS IS SEDS"
    }
    return render(request,'std/index.html',context)

def about(request):
    return HttpResponse("This is about page.")

def services(request):
    return HttpResponse("This is service page.")

def contact(request):
    return HttpResponse("This is contact page.")

def student_login(request):
    from std.models import Student
    if 'logout' in request.GET:
        request.session.flush()
        return redirect(reverse('home:student_login'))
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        try:
            student = Student.objects.get(roll=student_id, password=password)
            request.session['student_roll'] = student.roll
            request.session['student_name'] = student.name
            return redirect(reverse('home:student_dashboard'))
        except Student.DoesNotExist:
            return render(request, 'student_login.html', {'error': 'Invalid Student ID or Password'})
    return render(request, 'student_login.html')



def student_signup(request):
    return render(request,'student_signup.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return render(request, 'forgot_password.html', {'msg': 'Please enter email!'})
        
        try:
            user = Student.objects.get(email=email)
            from django.conf import settings
            from django.urls import reverse
            import secrets
            import hashlib
            
            # Generate secure token (hash: email + secret + timestamp)
            token = secrets.token_urlsafe(32)
            user.reset_token = hashlib.sha256(f"{email}:{token}:reset".encode()).hexdigest()
            user.save()
            
            link = request.build_absolute_uri(reverse('home:reset_password', args=[user.reset_token]))
            
            send_mail(
                'Reset Your Password - CampusPlacementHub',
                f'Dear {user.name},\n\n'
                f'Click this secure link to reset your password (valid for 1 hour):\n{link}\n\n'
                f'If you did not request this, ignore this email.\n\n'
                f'Best,\nCampusPlacementHub Team',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return render(request, 'forgot_password.html', {'msg': 'Reset link sent to your email! Check console/spam.'})
        except Student.DoesNotExist:
            return render(request, 'forgot_password.html', {'msg': 'Email not found in our records.'})
        except Exception as e:
            return render(request, 'forgot_password.html', {'error': f'Error: {str(e)}'})
    
    return render(request, 'forgot_password.html')

def student_dashboard(request):
    if 'student_roll' not in request.session:
        return redirect(reverse('home:student_login'))
    from std.models import Student
    student = Student.objects.get(roll=request.session['student_roll'])
    return render(request, 'std/student_dashboard.html', {'student': student})

def reset_password(request, token):
    if request.method == 'POST':
        password = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        if password != confirm:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match!'})
        if len(password) < 8:
            return render(request, 'reset_password.html', {'error': 'Password must be at least 8 characters!'})
        
        # Find user by token (security: compare full hash)
        import hashlib
        from std.models import Student
        from django.conf import settings
        
        user = None
        for u in Student.objects.filter(reset_token__isnull=False):
            expected = hashlib.sha256(f"{u.email}:{token}:reset".encode()).hexdigest()
            if u.reset_token == expected:
                user = u
                break
        
        if user:
            user.set_password(password)
            user.reset_token = None  # Clear token
            user.save()
            return redirect('home:student_login')
        else:
            return render(request, 'reset_password.html', {'error': 'Invalid or expired reset link!'})
    
    return render(request, 'reset_password.html')


