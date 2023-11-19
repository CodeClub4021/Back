from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Gym(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField()
    rate = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RATING_CHOICES
    )
    def __str__(self):
        return self.name
