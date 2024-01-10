from rest_framework import serializers
from users.models import CustomUser


class GymFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    rating = serializers.IntegerField(required=False, min_value=1, max_value=5)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'