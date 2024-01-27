from .models import User, Gym, Customer, Coach, Manager
from .serializers import UserSerializer, GymSerializer, CustomerSerializer, CoachSerializer, ManagerSerializer, CustomerGymJoinSerializer
from gymlist.permissions import IsManagerAndOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView


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

     
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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

class CurrentUser(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            related_model = None
            related_serializer = None

            if user.role == 'customer':
                related_model = Customer.objects.get(user=user)
                related_serializer = CustomerSerializer(related_model)
            elif user.role == 'coach':
                related_model = Coach.objects.get(user=user)
                related_serializer = CoachSerializer(related_model)
            elif user.role == 'manager':
                related_model = Manager.objects.get(user=user)
                related_serializer = ManagerSerializer(related_model)

            user_serializer = UserSerializer(user)

            return Response({'user': user_serializer.data, user.role: related_serializer.data if related_model else None}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED) 

class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ManagerList(generics.ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

class CoachList(generics.ListAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer


class CustomerJoinGymView(generics.CreateAPIView):
    serializer_class = CustomerGymJoinSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({"detail": "You have successfully joined the gym."}, status=status.HTTP_201_CREATED)

class CustomerJoinedGymsView(generics.ListAPIView):
    serializer_class = GymSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return customer.gyms.all()