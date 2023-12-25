from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from gyms.models import CustomUser
from .serializers import UserSerializer, ManagerInfoSerializer, CoachInfoSerializer, ChangePasswordSerializer
from django.contrib.auth.hashers import check_password
from django.core.exceptions import PermissionDenied

class CoachInfoEditView(generics.UpdateAPIView):
    def authenticate(self, gym, request, *args, **kwargs):
        if self.request.user_type!= 'coach':
            raise PermissionDenied("You do not have permission to perform this action.")
    
    queryset = CustomUser.objects.filter(user_type='coach')
    serializer_class = CoachInfoSerializer
    permission_classes = [permissions.IsAuthenticated] 

class ManagerInfoEditView(generics.UpdateAPIView):
    def authenticate(self, gym, request, *args, **kwargs):
        if self.request.user_type!= 'manager':
            raise PermissionDenied("You do not have permission to perform this action.")
        
    queryset = CustomUser.objects.filter(user_type='manager')
    serializer_class = ManagerInfoSerializer
    permission_classes = [permissions.IsAuthenticated] 

class UserSignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
class UserLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get('refresh')
        access = response.data.get('access')

        if refresh and access:
            refresh_token = RefreshToken(refresh)
            response.data['refresh_token'] = str(refresh_token.access_token)

        return response
    

class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CustomUser.objects.get(username=serializer.validated_data['username'])
        old_password = serializer.validated_data.get("old_password")
        if not check_password(old_password, user.password):
            return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data.get("new_password"))
        user.save()

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)


"""class GetUserByTypeView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_type = self.kwargs.get('user_type')
        if user_type not in ['coach', 'manager', 'user']:
            return CustomUser.objects.none()

        if user_type == 'coach':
            return CustomUser.objects.filter(user_type='coach')
        elif user_type == 'manager':
            return CustomUser.objects.filter(user_type='manager')
        elif user_type == 'user':
            return CustomUser.objects.filter(user_type='user')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)"""
class GetUserByTypeView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)
    
        