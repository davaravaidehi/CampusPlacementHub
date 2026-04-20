from django.urls import path
from co_ordinatorapp import views

app_name = 'co_ordinatorapp'

urlpatterns = [
    path('coordinator_signup/',   views.coordinator_signup,   name='coordinator_signup'),
    path('coordinator_login/',    views.coordinator_login,    name='coordinator_login'),
    path('coordinator_dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    path('coordinator_profile/', views.coordinator_profile, name='coordinator_profile'),
]
