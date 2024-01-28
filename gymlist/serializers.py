from rest_framework import serializers
from gymlist.models import Gym
from gymlist.models import User 
from gymlist.models import Customer 
from gymlist.models import Coach 
from gymlist.models import Manager 

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone_number', 'sex', 'birthday', 'education', 'language', 'location', 'work_experience', 'full_name', 'more_description', 'weight', 'height']

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'user', 'phone_number', 'sex', 'birthday', 'education', 'language', 'location', 'work_experience', 'full_name', 'more_description']

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ['id', 'user', 'phone_number', 'sex', 'birthday', 'education', 'language', 'location', 'work_experience', 'full_name', 'more_description']


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id', 'name', 'address', 'city', 'sex', 'since', 'work_hours', 'tier1_tuition', 'tier2_tuition', 'tier3_tuition', 'phone_number']
        
    def to_representation(self, instance):
        customer_count = instance.customers.count()
        coach_count = instance.coaches.count()

        data = super().to_representation(instance)

        data['customer_count'] = customer_count
        data['coach_count'] = coach_count

        return data

class CustomerGymJoinSerializer(serializers.Serializer):
    gym_id = serializers.PrimaryKeyRelatedField(queryset=Gym.objects.all())
    selected_tier = serializers.IntegerField(required=False)
    def create(self, validated_data):
        user = self.context['request'].user
        gym = validated_data['gym_id']
        customer, created = Customer.objects.get_or_create(user=user)
        customer.gyms.add(gym)
        return customer

class CoachGymJoinSerializer(serializers.Serializer):
    gym_id = serializers.PrimaryKeyRelatedField(queryset=Gym.objects.all())
    def create(self, validated_data):
        user = self.context['request'].user
        gym = validated_data['gym_id']
        coach, created = Coach.objects.get_or_create(user=user)
        coach.gyms.add(gym)
        return coach