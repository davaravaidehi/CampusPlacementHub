from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Coordinator(models.Model):

    DEPARTMENT_CHOICES = [
        ('CMPICA',  'CMPICA'),
        ('CSPIT',   'CSPIT'),
        ('DEPSTAR', 'DEPSTAR'),
    ]

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True, related_name='coordinator_profile')
    first_name  = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    email       = models.EmailField(max_length=150, unique=True)
    phone       = models.CharField(max_length=10)
    department  = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    password    = models.CharField(max_length=128)   # stored as hash
    created_at  = models.DateTimeField(auto_now_add=True)

    # ── helpers ──────────────────────────────────────
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} ({self.department})"

    class Meta:
        db_table        = 'coordinator'
        verbose_name    = 'Coordinator'
        verbose_name_plural = 'Coordinators'

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as AuthUser

@receiver(post_save, sender=Coordinator)
def create_user_for_coordinator(sender, instance, created, **kwargs):
    if created and not instance.user:
        username = instance.email.split('@')[0] if instance.email else f"{instance.first_name}{instance.last_name}".replace(' ', '').lower()
        if not username:
            username = 'coordinator'
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
        Coordinator.objects.filter(pk=instance.pk).update(user=user)
