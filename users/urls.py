# gym_app/urls.py
from django.urls import path
from .views import UserSignUpView, UserLoginView


urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]
#     path('club/edit_manager/', views.edit_manager, name='edit_manager'),