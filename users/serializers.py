from rest_framework import serializers
from .models import CustomUser, CoachInfo, ManagerInfo

class CoachInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachInfo
        fields = ['gender', 'birthday', 'education', 'language', 'location', 'years_of_experience', 'description']

class ManagerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerInfo
        fields = ['gender', 'birthday', 'education', 'language', 'location', 'years_of_experience', 'description']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'user_type']

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
             
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    username     = serializers.CharField(write_only=True, required=True)
