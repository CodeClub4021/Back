from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer, ManagerInfoSerializer, CoachInfoSerializer, ChangePasswordSerializer
from django.contrib.auth.hashers import check_password

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
