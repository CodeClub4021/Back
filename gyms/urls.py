from django.urls import path
from .views import GymListCreateView, GymDetailView, RatingCreateView, RatingListView, CoachCreateView, GymRegisteration, CoachRegistrationView

urlpatterns = [
    path('gyms/', GymListCreateView.as_view(), name='gym-list-create'),
    path('gyms/<int:pk>/', GymDetailView.as_view(), name='gym-detail'),
    path('gyms/<int:pk>/ratings/', RatingCreateView.as_view(), name='rating-create'),
    path('ratings/', RatingListView.as_view(), name='rating-list'),
    path('gyms/<int:pk>/add-coach/', CoachCreateView.as_view(), name='add-coach'),
    path('gyms/<int:pk>/users-reg/', GymRegisteration.as_view(), name='users-reg'),
    path('gyms/<int:gym_id>/register-coach/', CoachRegistrationView.as_view(), name='register-coach'),

]

