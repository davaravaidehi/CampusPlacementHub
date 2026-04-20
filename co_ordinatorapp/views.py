from django.shortcuts import render, redirect
from django.urls import reverse
from co_ordinatorapp.models import Coordinator
from std.models import Student


# ─────────────────────────────────────────────────────────────
#  SIGNUP  →  GET  : show form
#             POST : validate → save → redirect to login
# ─────────────────────────────────────────────────────────────
def coordinator_signup(request):
    if request.method == 'POST':
        first_name    = request.POST.get('first_name', '').strip()
        last_name     = request.POST.get('last_name',  '').strip()
        email         = request.POST.get('email',      '').strip()
        phone         = request.POST.get('phone',      '').strip()
        department    = request.POST.get('department', '').strip()
        password      = request.POST.get('password',         '')
        confirm_pass  = request.POST.get('confirm_password', '')

        # ── validation ───────────────────────────────
        errors = {}

        if not first_name:
            errors['first_name'] = 'First name is required.'

        if not last_name:
            errors['last_name'] = 'Last name is required.'

        if not email:
            errors['email'] = 'Email is required.'
        elif Coordinator.objects.filter(email=email).exists():
            errors['email'] = 'An account with this email already exists.'

        if not phone:
            errors['phone'] = 'Phone number is required.'
        elif not phone.isdigit() or len(phone) != 10:
            errors['phone'] = 'Enter a valid 10-digit phone number.'

        if not department:
            errors['department'] = 'Please select a department.'

        if not password:
            errors['password'] = 'Password is required.'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters.'

        if password != confirm_pass:
            errors['confirm_password'] = 'Passwords do not match.'

        if errors:
            return render(request, 'co-ordinator/coordinator_signup.html', {
                'errors':    errors,
                'form_data': request.POST,   # repopulate fields on error
            })

        # ── save ─────────────────────────────────────
        coordinator = Coordinator(
            first_name = first_name,
            last_name  = last_name,
            email      = email,
            phone      = phone,
            department = department,
        )
        coordinator.set_password(password)   # hashes the password
        coordinator.save()

        # redirect to login after successful registration
        return redirect(reverse('co_ordinatorapp:coordinator_login'))

    # GET – just show the blank form
    return render(request, 'co-ordinator/coordinator_signup.html')


# ─────────────────────────────────────────────────────────────
#  LOGIN   →  GET  : show login form
#             POST : authenticate → set session → dashboard
#             GET ?logout=1 : flush session → back to login
# ─────────────────────────────────────────────────────────────
def coordinator_login(request):
    if 'logout' in request.GET:
        request.session.flush()
        return redirect(reverse('co_ordinatorapp:coordinator_login'))

    if request.method == 'POST':
        identifier = request.POST.get('coordinator_id', '').strip()
        password   = request.POST.get('password', '')

        try:
            coordinator = Coordinator.objects.get(email=identifier)
        except Coordinator.DoesNotExist:
            return render(request, 'co-ordinator/coordinator_login.html', {
                'error': 'Invalid email or password.'
            })

        if coordinator.check_password(password):
            # store coordinator info in session
            request.session['coordinator_id']   = coordinator.id
            request.session['coordinator_name'] = coordinator.full_name
            request.session['coordinator_dept'] = coordinator.department

            # redirect to coordinator dashboard
            return redirect(reverse('co_ordinatorapp:coordinator_dashboard'))
        else:
            return render(request, 'co-ordinator/coordinator_login.html', {
                'error': 'Invalid email or password.'
            })

    return render(request, 'co-ordinator/coordinator_login.html')


# ─────────────────────────────────────────────────────────────
#  DASHBOARD  →  session-protected
# ─────────────────────────────────────────────────────────────
def coordinator_profile(request):
    if 'coordinator_id' not in request.session:
        return redirect(reverse('co_ordinatorapp:coordinator_login'))

    coordinator = Coordinator.objects.get(id=request.session['coordinator_id'])
    return render(request, 'co-ordinator/coordinator_profile.html', {'coordinator': coordinator})

def coordinator_dashboard(request):
    if 'coordinator_id' not in request.session:
        return redirect(reverse('co_ordinatorapp:coordinator_login'))

    coordinator = Coordinator.objects.get(id=request.session['coordinator_id'])
    
    total_students = Student.objects.filter(department=coordinator.department).count()
    active_drives = 8  # Placeholder for active placement drives
    placed_students = 23  # Placeholder for placed students
    
    recent_students = list(Student.objects.filter(department=coordinator.department)
                          .values('roll', 'name', 'email')[:5])
    
    # Mock data for expanded design (active/upcoming/overdue companies, placed, applications)
    companies = [
        {'name': 'TCS', 'date': '2024-10-10', 'status': 'active', 'students_applied': 45},
        {'name': 'Infosys', 'date': '2024-10-12', 'status': 'active', 'students_applied': 32},
        {'name': 'Wipro', 'date': '2024-10-15', 'status': 'upcoming', 'students_applied': 28},
        {'name': 'Accenture', 'date': '2024-10-08', 'status': 'overdue', 'students_applied': 19},
        {'name': 'Capgemini', 'date': '2024-10-20', 'status': 'upcoming', 'students_applied': 51},
    ]
    
    placed_students_detail = [
        {'student_roll': 'CMP001', 'student_name': 'John Doe', 'company': 'TCS', 'date': '2024-09-25'},
        {'student_roll': 'CMP002', 'student_name': 'Jane Smith', 'company': 'Infosys', 'date': '2024-09-28'},
        {'student_roll': 'CMP003', 'student_name': 'Bob Johnson', 'company': 'Wipro', 'date': '2024-10-01'},
    ]
    
    applications = [
        {'student_roll': 'CMP004', 'student_name': 'Alice Brown', 'company': 'TCS', 'status': 'pending'},
        {'student_roll': 'CMP005', 'student_name': 'Charlie Wilson', 'company': 'Infosys', 'status': 'shortlisted'},
        {'student_roll': 'CMP006', 'student_name': 'Diana Davis', 'company': 'Accenture', 'status': 'rejected'},
    ]
    
    context = {
        'coordinator': coordinator,
        'total_students': total_students,
        'active_drives': active_drives,
        'placed_students': placed_students,
        'recent_students': recent_students,
        'placement_rate': round((placed_students / total_students * 100), 1) if total_students > 0 else 0,
        'companies': companies,
        'placed_students_detail': placed_students_detail,
        'applications': applications,
    }
    return render(request, 'co-ordinator/coordinator_dashboard.html', context)
