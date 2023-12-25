from django.urls import path
from .views import GymFilterView

urlpatterns = [
    path('mainpage/gym_filter/', GymFilterView.as_view(), name='gym-filter'),
]
