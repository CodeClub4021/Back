from rest_framework import serializers
from .models import Gym
from rest_framework import serializers
from users.serializers import CustomUser
from .models import Gym, Rating


class GymSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    coaches = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username', many=True)

    class Meta:
        model = Gym
        fields = ['name', 'address', 'city', 'manager', 'coaches']

    def create(self, validated_data):
        coaches_data = validated_data.pop('coaches')
        gym = Gym.objects.create(**validated_data)
        gym.coaches.set(coaches_data)
        return gym

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'



# from rest_framework import serializers
# from .models import Gym, GymRating

# class GymSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Gym
#         fields = ['id', 'name', 'address', 'manager', 'coaches']

# class GymRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GymRating
#         fields = ['id', 'gym', 'user', 'rating']
