from django.db import models

class CollegeAdmin(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True, related_name='collegeadmin_profile')
    full_name    = models.CharField(max_length=100)
    email        = models.EmailField(max_length=150, unique=True)
    password     = models.CharField(max_length=128) 
    college_name = models.CharField(max_length=200)
 
    def __str__(self):
        return f"{self.full_name} – {self.college_name}"

# Add this new model
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    institute = models.ForeignKey('Institute', on_delete=models.CASCADE, null=True, blank=True)
    name         = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Institute(models.Model):
    institute_id = models.AutoField(primary_key=True)
    institute_name = models.CharField(max_length=200)

    def __str__(self):
        return self.institute_name

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as AuthUser

@receiver(post_save, sender=CollegeAdmin)
def create_user_for_college_admin(sender, instance, created, **kwargs):
    if created and not instance.user:
        username = instance.email.split('@')[0] if instance.email else instance.full_name.replace(' ', '').lower()
        if not username:
            username = 'admin'
        base_username = username
        counter = 1
        while AuthUser.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
            
        user = AuthUser.objects.create_user(
            username=username,
            email=instance.email,
            password=instance.password
        )
        user.is_staff = True  # College admins might need staff access to login to admin panel depending on their setup
        user.save()
        CollegeAdmin.objects.filter(pk=instance.pk).update(user=user)