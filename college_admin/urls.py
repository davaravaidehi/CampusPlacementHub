from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('register/', views.admin_register, name='admin_register'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('list/', views.admin_list, name='admin_list'),
    path('update/<int:admin_id>/', views.update_admin, name='update_admin'),
    path('do_update/<int:admin_id>/', views.do_update_admin, name='do_update_admin'),
    path('delete/<int:admin_id>/', views.delete_admin, name='delete_admin'),
    path('departments/', views.departments, name='departments'),
    path('add-department/', views.add_department, name='add_department'),
    path('delete-department/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('update-department/<int:dept_id>/', views.update_department, name='update_department'),
    path('institutes/', views.institutes, name='institutes'),
    path('institutes/<int:id>/', views.institute_detail, name='institute_detail'),
    path('delete-institute/<int:id>/', views.delete_institute, name='delete_institute'),
]