from rest_framework import serializers

class GymFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    rating = serializers.IntegerField(required=False, min_value=1, max_value=5)