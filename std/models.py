from django.db import models
from django.utils import timezone

class Student(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True, related_name='student_profile')
    roll=models.CharField(max_length=100, unique=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=150, unique=True)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=200)
    department = models.CharField(max_length=50, default='')
    course = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=128)
    reset_token = models.CharField(max_length=64, null=True, blank=True)
    reset_token_expiry = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.reset_token and not self.reset_token_expiry:
            self.reset_token_expiry = timezone.now() + timezone.timedelta(hours=1)
        elif self.pk and not self.reset_token:
            self.reset_token = None
            self.reset_token_expiry = None
        super().save(*args, **kwargs)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as AuthUser

@receiver(post_save, sender=Student)
def create_user_for_student(sender, instance, created, **kwargs):
    if created and not instance.user:
        username = instance.email.split('@')[0] if instance.email else instance.name.replace(' ', '').lower()
        if not username:
            username = 'student'
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
        Student.objects.filter(pk=instance.pk).update(user=user)
