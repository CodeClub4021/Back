from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coach(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

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
    coach = models.ForeignKey(Coach, related_name='ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.coach.name} - {self.rating}"