from django.db import models
from users.models import CustomUser
from django.utils import timezone



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
    



class GymComment(models.Model):
    gym = models.ForeignKey('Gym', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.gym.name} - {self.created_at}"



class GymProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    exercises = models.TextField()  # Store exercises as a comma-separated string

    def __str__(self):
        return self.name
    
    

# # from django.db import models
# # from users.models import CustomUser  

# # class Gym(models.Model):
# #     name = models.CharField(max_length=100)
# #     address = models.CharField(max_length=255)
# #     manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_gyms')
# #     coaches = models.ManyToManyField(CustomUser, related_name='coached_gyms', blank=True)

# # class GymRating(models.Model):
# #     gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='ratings')
# #     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
# #     rating = models.IntegerField()


# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator

# """
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     gyms = models.ManyToManyField('Gym', related_name='memberships')
# """

# class Gym(models.Model):
#     RATING_CHOICES = [
#         (1, '1'),
#         (2, '2'),
#         (3, '3'),
#         (4, '4'),
#         (5, '5'),
#     ]

#     name = models.CharField(max_length=255, unique=True)
#     address = models.TextField()
#     """rate = models.DecimalField(
#         max_digits=1,
#         decimal_places=0,
#         validators=[MinValueValidator(1), MaxValueValidator(5)],
#         choices=RATING_CHOICES
#     )"""
#     def __str__(self):
#         return self.name


#     @property
#     def average_rating(self):
#         ratings = self.ratings.all()
#         if ratings:
#             return sum(rating.rating for rating in ratings) / len(ratings)
#         return 0

#     def __str__(self):
#         return self.name

# class Rating(models.Model):
#     gym = models.ForeignKey(Gym, related_name='ratings', on_delete=models.CASCADE)
#     rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

#     def __str__(self):
#         return f"{self.gym.name} - {self.rating}"