from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gyms = models.ManyToManyField('Gym', related_name='memberships')
"""

class Gym(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    ]

    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    """rate = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RATING_CHOICES
    )"""
    def __str__(self):
        return self.name


    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

    def __str__(self):
        return self.name

class Rating(models.Model):
    gym = models.ForeignKey(Gym, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])

    def __str__(self):
        return f"{self.gym.name} - {self.rating}"