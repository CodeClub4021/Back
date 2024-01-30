from .models import User, Gym, Customer, Coach, Manager, GymRating, CoachRating
from .serializers import CoachRatingSerializer, UserSerializer, GymSerializer, CustomerSerializer, CoachSerializer, ManagerSerializer, CoachGymJoinSerializer, CustomerGymJoinSerializer, PasswordChangeSerializer, GymRatingSerializer
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
from rest_framework.exceptions import ValidationError

class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        confirm_password = serializer.validated_data['confirm_password']

        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'detail': 'New password and confirmation do not match.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password has been successfully changed.'}, status=status.HTTP_200_OK)

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
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Annotate the instance with customer and coach counts
        instance.customer_count = instance.customers.count()
        instance.coach_count = instance.coaches.count()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class GymRatingCreateView(generics.CreateAPIView):
    serializer_class = GymRatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        customer = self.request.user

        if customer.role != 'customer':
            raise ValidationError("Only customers can rate gyms.")

        gym_id = self.request.data.get('gym_id', None)
        rating = self.request.data.get('rating', 5)
        
        if gym_id:
            try:
                gym = Gym.objects.get(id=gym_id)
            except Gym.DoesNotExist:
                raise ValidationError("Invalid gym ID.")
            
            existing_rating = GymRating.objects.filter(customer=customer, gym=gym).first()
            if existing_rating:
                raise ValidationError("You have already rated this gym.")
            if not gym.customers.filter(user=customer).exists():
                raise ValidationError("You can only rate gyms where you are a member.")
            
            serializer.save(customer=customer, gym=gym, rating=rating)
        else:
            raise ValidationError("The 'gym' field is required.")

class CoachRatingCreateView(generics.CreateAPIView):
    queryset = CoachRating.objects.all()
    serializer_class = CoachRatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        coach_id = request.data.get('coach_id', None)

        if not coach_id:
            return Response({'error': 'coach_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coach = Coach.objects.get(pk=coach_id)
        except Coach.DoesNotExist:
            return Response({'error': 'Coach not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the customer has already rated the coach
        existing_rating = CoachRating.objects.filter(customer=request.user, coach=coach)
        if existing_rating.exists():
            return Response({'error': 'You have already rated this coach.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(customer=request.user, coach=coach)

        return Response(serializer.data, status=status.HTTP_201_CREATED)        
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

class CustomerUpdateView(generics.UpdateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if user.role != 'customer':
            return None

        customer, created = Customer.objects.get_or_create(user=user)
        return customer

    def update(self, request, *args, **kwargs):
        customer = self.get_object()

        if not customer:
            return Response({"error": "You must have the 'customer' role to update your information."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your information has been updated successfully.", "customer" : serializer.data}, status=status.HTTP_200_OK)

class ManagerList(generics.ListAPIView):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer


class ManagerUpdateView(generics.UpdateAPIView):
    serializer_class = ManagerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if user.role != 'manager':
            return None

        manager, created = Manager.objects.get_or_create(user=user)
        return manager

    def update(self, request, *args, **kwargs):
        manager = self.get_object()

        if not manager:
            return Response({"error": "You must have the 'manager' role to update your information."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(manager, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your information has been updated successfully.", "manager" : serializer.data}, status=status.HTTP_200_OK)

class CoachList(generics.ListAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer

class CompletedInfoCoachListView(generics.ListAPIView):
    queryset = Coach.objects.filter(
        phone_number__isnull=False,
        sex__isnull=False,
        birthday__isnull=False,
        education__isnull=False,
        language__isnull=False,
        location__isnull=False,
        work_experience__isnull=False,
        full_name__isnull=False,
        more_description__isnull=False
    )
    serializer_class = CoachSerializer
    permission_classes = [IsAuthenticated]


class AddCoachToGymView(generics.UpdateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        coach_id = request.data.get('coach_id', None)
        gym = self.get_object()

        if not coach_id:
            return Response({'error': 'coach_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            coach = Coach.objects.get(pk=coach_id)
        except Coach.DoesNotExist:
            return Response({'error': 'Coach not found.'}, status=status.HTTP_404_NOT_FOUND)

        if gym.manager.user != request.user:
            return Response({'error': 'You are not the manager of this gym.'}, status=status.HTTP_403_FORBIDDEN)

        gym.coaches.add(coach)
        gym.save()

        serializer = self.get_serializer(gym)
        return Response(serializer.data)


class CoachUpdateView(generics.UpdateAPIView):
    serializer_class = CoachSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user

        if user.role != 'coach':
            return None

        coach, created = Coach.objects.get_or_create(user=user)
        return coach

    def update(self, request, *args, **kwargs):
        coach = self.get_object()

        if not coach:
            return Response({"error": "You must have the 'coach' role to update your information."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(coach, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your information has been updated successfully.", "coach" : serializer.data}, status=status.HTTP_200_OK)


class CustomerJoinGymView(generics.CreateAPIView):
    serializer_class = CustomerGymJoinSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        gym = serializer.validated_data['gym_id']
        selected_tier = serializer.validated_data.get('selected_tier', 1)  # Default to tier 1 if not provided

        user = self.request.user
        customer, created = Customer.objects.get_or_create(user=user)

        if (
            not customer.phone_number or
            not customer.sex or
            not customer.birthday or
            not customer.education or
            not customer.language or
            not customer.location or
            not customer.work_experience or
            not customer.full_name or
            not customer.more_description
        ):
            return Response({"error": "Please complete all fields in your profile before joining the gym."}, status=status.HTTP_400_BAD_REQUEST)

        tier_field_name = f'tier{selected_tier}_tuition'
        tier_tuition = getattr(gym, tier_field_name)
        if customer.wallet < tier_tuition:
            return Response({"error": "Insufficient wallet balance to join the selected tier."}, status=status.HTTP_400_BAD_REQUEST)

        customer.wallet -= tier_tuition
        customer.save()

        customer.gyms.add(gym)

        return Response({"detail": f"You have successfully joined the gym with Tier {selected_tier}."}, status=status.HTTP_201_CREATED)

class CustomerJoinedGymsView(generics.ListAPIView):
    serializer_class = GymSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = Customer.objects.get(user=self.request.user)
        return customer.gyms.all()

class CoachJoinGymView(generics.CreateAPIView):
    serializer_class = CoachGymJoinSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        gym = serializer.validated_data['gym_id']

        user = self.request.user
        coach, created = Coach.objects.get_or_create(user=user)

        if (
            not coach.phone_number or
            not coach.sex or
            not coach.birthday or
            not coach.education or
            not coach.language or
            not coach.location or
            not coach.work_experience or
            not coach.full_name or
            not coach.more_description
        ):
            return Response({"error": "Please complete all fields in your profile before joining the gym."}, status=status.HTTP_400_BAD_REQUEST)

        coach.gyms.add(gym)

        return Response({"detail": f"You have successfully joined the gym."}, status=status.HTTP_201_CREATED)

class CoachJoinedGymsView(generics.ListAPIView):
    serializer_class = GymSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        coach = Coach.objects.get(user=self.request.user)
        return coach.gyms.all()
    

class RemoveUserFromGymView(generics.UpdateAPIView):
    queryset = Gym.objects.all()
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user_id = request.data.get('user_id', None)

        if not user_id:
            return Response({'error': 'user_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            manager = Manager.objects.get(user=request.user)
        except Manager.DoesNotExist:
            return Response({'error': 'You are not authorized to manage gyms.'}, status=status.HTTP_403_FORBIDDEN)

        manager_gym = manager.gym
        if(not manager.gym):
            return Response({'error': 'You dont have a gym'}, status=status.HTTP_400_FORBIDDEN)

        if user.role == 'coach':
            manager_gym.coaches.remove(user.coach)
        elif user.role == 'customer':
            manager_gym.customers.remove(user.customer)

        manager_gym.refresh_from_db()
        return Response({'message': 'User removed from the gym successfully.'}, status=status.HTTP_200_OK)