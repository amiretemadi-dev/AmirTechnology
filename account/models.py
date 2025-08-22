from django.db import models
from django.contrib.auth.models import AbstractUser
import random, string
from django.utils import timezone


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    image_profile = models.ImageField(upload_to='images/users', blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class VerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.digits, k=6))

        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() <= self.expires_at

    def __str__(self):
        return f"Code {self.code} for {self.email}"
