from django.urls import path
from .views import GymFilterView, AdminUserInfoView, CoachUserInfoView

urlpatterns = [
    path('mainpage/gym_filter/', GymFilterView.as_view(), name='gym-filter'),
    path('mainpage/user/<int:user_id>/', AdminUserInfoView.as_view(), name='admin_user_info'),
    path('mainpage/user/<int:user_id>/', CoachUserInfoView.as_view(), name='coach_user_info'),
]
