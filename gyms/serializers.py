from rest_framework import serializers
from .models import Gym
from rest_framework import serializers
from users.serializers import CustomUser
from .models import Gym, Rating


class GymSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username')
    coaches = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username', many=True)
    users   = serializers.SlugRelatedField(queryset=CustomUser.objects.all(), slug_field='username', many=True)

    class Meta:
        model = Gym
        fields = ['name', 'address', 'city', 'manager', 'coaches', 'users']

    def create(self, validated_data):
        coaches_data = validated_data.pop('coaches')
        users_data = validated_data.pop('users', [])
        gym = Gym.objects.create(**validated_data)
        gym.coaches.set(coaches_data)
        gym.users.set(users_data)
        return gym
    
class CoachRegistrationSerializer(serializers.Serializer):
    coach_request = serializers.BooleanField()
    def post(self, request, gym_id):
        serializer = CoachRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
class CoachCreateSerializer(serializers.Serializer):
    coach_username = serializers.CharField()

class UserRegisterSerializer(serializers.Serializer):
    user_username = serializers.CharField()


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
