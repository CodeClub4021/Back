from django.db import models
from users.models import CustomUser


class Gym(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default='YourDefaultCity')
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_gym', limit_choices_to={'role': 'manager'}, default=1)
    coaches = models.ManyToManyField(CustomUser, related_name='coached_gyms', limit_choices_to={'role': 'coach'})
    users   = models.ManyToManyField(CustomUser, related_name='gym_users', limit_choices_to={'role': 'user'})

    def __str__(self):
        return self.name


class Rating(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.gym.name} - {self.rating}'
