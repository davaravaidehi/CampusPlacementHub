from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contact", views.contact, name='contact'),
    path("student_login", views.student_login, name='student_login'),
    path("placement_login", views.placement_login, name='placement_login'),
    path("student_signup", views.student_signup, name='student_signup'),
    path("forgot_password", views.forgot_password, name='forgot_password'),
    path("university_dashboard", views.university_dashboard, name='university_dashboard'),
]
