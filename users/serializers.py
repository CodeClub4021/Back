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
    # coach_info = CoachInfoSerializer(required=False)
    # manager_info = ManagerInfoSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'user_type']

    def create(self, validated_data):
        # coach_info_data = validated_data.pop('coach_info', None)
        # manager_info_data = validated_data.pop('manager_info', None)

        # user = CustomUser.objects.create(**validated_data)
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=validated_data['user_type']
        )
        # if user.user_type == 'coach' and coach_info_data:
        #     CoachInfo.objects.create(user=user, **coach_info_data)
        # elif user.user_type == 'manager' and manager_info_data:
        #     ManagerInfo.objects.create(user=user, **manager_info_data)
        user.set_password(validated_data['password'])
        user.save()
             
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    username     = serializers.CharField(write_only=True, required=True)
