from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from gyms.models import Gym, Rating
from .serializers import GymFilterSerializer

class GymFilterView(APIView):
    def get(self, request):
        serializer = GymFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        gyms = Gym.objects.all()

        name = serializer.validated_data.get('name')
        if name:
            gyms = gyms.filter(name__icontains=name)

        city = serializer.validated_data.get('city')
        if city:
            gyms = gyms.filter(city__icontains=city)

        rating = serializer.validated_data.get('rating')
        if rating:
            gyms = gyms.filter(ratings__rating=rating)

        gym_data = [{'name': gym.name, 'city': gym.city, 'rating': gym.get_average_rating()} for gym in gyms]
        return Response(gym_data, status=status.HTTP_200_OK)
