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

    def get_coach_info(self):
        if self.user_type == 'coach':
            return self.coach_info
        return None

    def get_manager_info(self):
        if self.user_type == 'manager':
            return self.manager_info
        return None


from django.db import models
from django.contrib.auth.models import AbstractUser

class CoachInfo(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='coach_info')
    username = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birthday = models.DateField()
    education = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    description = models.TextField()

class ManagerInfo(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='manager_info')
    username = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birthday = models.DateField()
    education = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    description = models.TextField()
