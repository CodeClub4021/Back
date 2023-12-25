from rest_framework import serializers
from .models import CustomUser, CoachInfo, ManagerInfo

class CoachInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachInfo
        fields = ['username', 'gender', 'birthday', 'education', 'language', 'location', 'years_of_experience', 'description']

class ManagerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerInfo
        fields = ['username', 'gender', 'birthday', 'education', 'language', 'location', 'years_of_experience', 'description']

class UserSerializer(serializers.ModelSerializer):
    #coach_info = CoachInfoSerializer(required=True)
    #manager_info = ManagerInfoSerializer(required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'user_type']

    def create(self, validated_data):
        coach_info_data = validated_data.pop('coach_info')
        manager_info_data = validated_data.pop('manager_info')

        user = CustomUser.objects.create(**validated_data)

        if user.user_type == 'coach':
            CoachInfo.objects.create(user=user, **coach_info_data)
        elif user.user_type == 'manager':
            ManagerInfo.objects.create(user=user, **manager_info_data)

        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    username     = serializers.CharField(write_only=True, required=True)
