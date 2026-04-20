from django.urls import path
from . import views
app_name = 'std'

urlpatterns=[
    path("", views.home),
    path("home/", views.home),
    path("add-std/", views.std_app),
    path("delete-std/<int:roll>", views.delete_std),
    path("update-std/<int:roll>", views.update_std),
    path("do-update-std/<int:roll>", views.do_update_std),
# Removed forgot/reset password URLs - use home app instead
]
