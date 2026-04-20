from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Max
from .models import CollegeAdmin,Department,Institute
from django.shortcuts import get_object_or_404
 
# ─── Register Admin ──────────────────────────────────────────────────────────
def admin_register(request):
    if request.method == 'POST':
        full_name     = request.POST.get('full_name')
        email         = request.POST.get('email')
        password      = request.POST.get('password')
        confirm_pass  = request.POST.get('confirm_password')
        college_name  = request.POST.get('college_name')
 
        # Basic validations
        if password != confirm_pass:
            return render(request, 'college_admin/admin_register.html',
                          {'error': 'Passwords do not match!'})
 
        if CollegeAdmin.objects.filter(email=email).exists():
            return render(request, 'college_admin/admin_register.html',
                          {'error': 'Email already registered!'})
 
        admin = CollegeAdmin()
        admin.full_name    = full_name
        admin.email        = email
        admin.password     = password     # plain text – same approach as Student model
        admin.college_name = college_name
        admin.save()
 
        return redirect('/college_admin/login/')
 
    return render(request, 'college_admin/admin_register.html', {})
 
 
# ─── Login ────────────────────────────────────────────────────────────────────
def admin_login(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
 
        try:
            admin = CollegeAdmin.objects.get(email=email, password=password)
            # Save admin info in session
            request.session['admin_id']          = admin.id
            request.session['admin_name']        = admin.full_name
            request.session['admin_college']     = admin.college_name
            return redirect('admin_dashboard')
        except CollegeAdmin.DoesNotExist:
            return render(request, 'college_admin/admin_login.html',
                          {'error': 'Invalid email or password!'})
 
    return render(request, 'college_admin/admin_login.html', {})
 
 
# ─── Dashboard ───────────────────────────────────────────────────────────────
def admin_dashboard(request):
    if not request.session.get('admin_id'):
        return redirect('/college_admin/login/')
 
    admin = CollegeAdmin.objects.get(pk=request.session['admin_id'])
    
    inst_count = Institute.objects.count()
    dept_count = Department.objects.count()
    
    try:
        from co_ordinatorapp.models import Coordinator
        coord_count = Coordinator.objects.count()
    except Exception:
        coord_count = 0
        
    context = {
        'admin': admin,
        'inst_count': inst_count,
        'dept_count': dept_count,
        'coord_count': coord_count,
    }
    
    return render(request, 'college_admin/admin_dashboard.html', context)
 
 
# ─── Logout ───────────────────────────────────────────────────────────────────
def admin_logout(request):
    request.session.flush()
    return redirect('/college_admin/login/')
 
 
# ─── List all Admins ──────────────────────────────────────────────────────────
def admin_list(request):
    admins = CollegeAdmin.objects.all()
    return render(request, 'college_admin/admin_list.html', {'admins': admins})
 
 
# ─── Update Admin ─────────────────────────────────────────────────────────────
def update_admin(request, admin_id):
    admin = CollegeAdmin.objects.get(pk=admin_id)
    return render(request, 'college_admin/update_admin.html', {'admin': admin})
 
 
def do_update_admin(request, admin_id):
    full_name    = request.POST.get('full_name')
    email        = request.POST.get('email')
    college_name = request.POST.get('college_name')
 
    admin              = CollegeAdmin.objects.get(pk=admin_id)
    admin.full_name    = full_name
    admin.email        = email
    admin.college_name = college_name
    admin.save()
    return redirect('/college_admin/list/')
 
 
# ─── Delete Admin ─────────────────────────────────────────────────────────────
def delete_admin(request, admin_id):
    admin = CollegeAdmin.objects.get(pk=admin_id)
    admin.delete()
    return redirect('/college_admin/list/')


def departments(request):
    depts = Department.objects.all()
    institutes = Institute.objects.all()

    dept_count = depts.count()

    context = {
        'departments': depts,
        'institutes': institutes,
        'dept_count': dept_count,
    }

    return render(request, 'college_admin/departments.html', context)


def add_department(request):
    if request.method == 'POST':
        institute_id = request.POST.get('institute_id')
        dept_name = request.POST.get('dept_name')

        # Auto-increment department_id starting from 101
        max_id = Department.objects.aggregate(max_id=Max('department_id'))['max_id']
        dept_id = 101 if not max_id or max_id < 101 else None

        institute = None
        if institute_id:
            institute = Institute.objects.filter(institute_id=institute_id).first()

        if dept_id:
            Department.objects.create(
                department_id=dept_id,
                institute=institute,
                name=dept_name
            )
        else:
            Department.objects.create(
                institute=institute,
                name=dept_name
            )

        messages.success(request, "Department added successfully!")
        return redirect('departments')

    return redirect('departments')


def delete_department(request, dept_id):
    dept = get_object_or_404(Department, department_id=dept_id)
    dept.delete()
    messages.success(request, "Department deleted successfully!")
    return redirect('departments')


def update_department(request, dept_id):
    dept = get_object_or_404(Department, department_id=dept_id)

    if request.method == 'POST':
        dept.name = request.POST.get('dept_name')
        dept.save()

        messages.success(request, "Department updated successfully!")
        return redirect('departments')

    return render(
        request,
        'college_admin/update_department.html',
        {'dept': dept}
    )



def institutes(request):
    if request.method == "POST":
        institute_name = request.POST.get("institute_name")

        max_id = Institute.objects.aggregate(max_id=Max('institute_id'))['max_id']
        if not max_id or max_id < 1001:
            Institute.objects.create(
                institute_id=1001,
                institute_name=institute_name
            )
        else:
            Institute.objects.create(
                institute_name=institute_name
            )

        return redirect("institutes")

    data = Institute.objects.all()
    return render(request, "college_admin/institutes.html", {"institutes": data})

def institute_detail(request, id):
    institute = get_object_or_404(Institute, institute_id=id)
    departments = Department.objects.filter(institute=institute)
    dept_count = departments.count()
    return render(request, "college_admin/institute_detail.html", {
        "institute": institute,
        "departments": departments,
        "dept_count": dept_count,
    })

def delete_institute(request, id):
    institute = get_object_or_404(Institute, institute_id=id)
    institute.delete()
    messages.success(request, "Institute deleted successfully!")
    return redirect('institutes')