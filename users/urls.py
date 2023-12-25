from django.urls import path
from .views import UserSignUpView, UserLoginView, CoachInfoEditView, ManagerInfoEditView, ChangePasswordView


urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('coach/edit/', CoachInfoEditView.as_view(), name='coach-info-edit'),
    path('manager/edit/', ManagerInfoEditView.as_view(), name='manager-info-edit'),
    path('changepassword', ChangePasswordView.as_view(), name='change-password'),
]
