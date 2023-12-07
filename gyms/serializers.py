from rest_framework import serializers
from .models import Gym, GymRating

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id', 'name', 'address', 'manager', 'coaches']

class GymRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymRating
        fields = ['id', 'gym', 'user', 'rating']
