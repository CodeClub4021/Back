from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer, ManagerInfoSerializer, CoachInfoSerializer

class CoachInfoEditView(generics.UpdateAPIView):
    queryset = CustomUser.objects.filter(user_type='coach')
    serializer_class = CoachInfoSerializer
    permission_classes = [permissions.IsAuthenticated] 

class ManagerInfoEditView(generics.UpdateAPIView):
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
