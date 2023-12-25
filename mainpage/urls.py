from django.urls import path
from .views import GymFilterView

urlpatterns = [
    path('gyms/filter/', GymFilterView.as_view(), name='gym-filter'),
]
