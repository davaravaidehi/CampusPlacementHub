from django.contrib.auth.models import User as AuthUser

class User(AuthUser):
    class Meta:
        proxy = True
        app_label = 'home'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
