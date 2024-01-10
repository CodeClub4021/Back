from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    USER_TYPES = (
        ('manager', 'Manager'),
        ('coach', 'Coach'),
        ('user', 'User'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    groups = models.ManyToManyField('auth.Group', related_name='customuser_set', blank=True, verbose_name='groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_set', blank=True, verbose_name='user permissions')


    age = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)

