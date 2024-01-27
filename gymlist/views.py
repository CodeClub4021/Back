from gymlist.models import Gym
from gymlist.models import User
from gymlist.serializers import GymSerializer
from gymlist.serializers import UserSerializer
from gymlist.serializers import CustomerSerializer
from gymlist.serializers import CoachSerializer
from gymlist.serializers import ManagerSerializer
from gymlist.permissions import IsManagerAndOwnerOrReadOnly

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class GymList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Gym.objects.all()
    serializer_class = GymSerializer

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'manager':
            serializer.save(manager=user.manager)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'فقط مدیران میتوانند باشگاه جدید ایجاد کنند.'}, status=status.HTTP_403_FORBIDDEN)


class GymDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsManagerAndOwnerOrReadOnly]
    queryset = Gym.objects.all()
    serializer_class = GymSerializer


class RegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
       
    def perform_create(self, serializer):
        user = serializer.save()
        role = serializer.validated_data.get('role')

        if role == 'customer':
            customer_serializer = CustomerSerializer(data={'user': user.id})
            if customer_serializer.is_valid():
                customer_serializer.save()
            else:
                user.delete()
                return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif role == 'manager':
            manager_serializer = ManagerSerializer(data={'user': user.id})
            if manager_serializer.is_valid():
                manager_serializer.save()
            else:
                user.delete()
                return Response(manager_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif role == 'coach':
            coach_serializer = CoachSerializer(data={'user': user.id})
            if coach_serializer.is_valid():
                coach_serializer.save()
            else:
                user.delete()
                return Response(coach_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response_data = {'id': user.id, **serializer.data}

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username is None or password is None:
            return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)