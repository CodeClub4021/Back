from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role_choices = [
        ('coach', 'Coach'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=10, choices=role_choices)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [] 
    def __str__(self):
        return self.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coaches = models.ManyToManyField('Coach', related_name='my_customers')
    gyms = models.ManyToManyField('Gym', related_name='memberships')

    phone_number = models.CharField(max_length=15, null=True)
    sex = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)
    education = models.CharField(max_length=255, null=True)
    language = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    work_experience = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    more_description = models.TextField(null=True)

    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def clean(self):
        if self.user.role != 'customer':
            raise ValidationError("Only users with the 'customer' role can be assigned as customers.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Coach(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gyms = models.ManyToManyField('Gym', related_name='gym_coaches')
    customers = models.ManyToManyField(Customer, related_name='my_coaches')

    phone_number = models.CharField(max_length=15, null=True)
    sex = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)
    education = models.CharField(max_length=255, null=True)
    language = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    work_experience = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    more_description = models.TextField(null=True)


    def clean(self):
        if self.user.role != 'coach':
            raise ValidationError("Only users with the 'coach' role can be assigned as coaches.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=15, null=True)
    sex = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)
    education = models.CharField(max_length=255, null=True)
    language = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    work_experience = models.CharField(max_length=255, null=True)
    full_name = models.CharField(max_length=255, null=True)
    more_description = models.TextField(null=True)

    def clean(self):
        if self.user.role != 'manager':
            raise ValidationError("Only users with the 'manager' role can be assigned as managers.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class GymPicture(models.Model):
    gym = models.ForeignKey('Gym', on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to='gym_pictures')


class Gym(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default='Tehran')
    manager = models.OneToOneField(Manager, on_delete=models.CASCADE)
    coaches = models.ManyToManyField(Coach)
    customers = models.ManyToManyField(Customer)

    sex = models.CharField(max_length=10, null=True)
    since = models.DateField(null=True)
    work_hours = models.CharField(max_length=255, null=True)
    tuition = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    phone_number = models.CharField(max_length=15, null=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.gym.name} - {self.rating}'