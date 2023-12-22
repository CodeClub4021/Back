# gym_app/urls.py
from django.urls import path
from .views import UserSignUpView, UserLoginView, CoachInfoEditView, ManagerInfoEditView


urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('coach/edit/', CoachInfoEditView.as_view(), name='coach-info-edit'),
    path('manager/edit/', ManagerInfoEditView.as_view(), name='manager-info-edit'),
]
#     path('club/edit_manager/', views.edit_manager, name='edit_manager'),