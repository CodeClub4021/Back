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



# # from django.urls import path
# # from .views import GymView, GymDetailView, GymRatingView

# # urlpatterns = [
# #     path('gyms/', GymView.as_view(), name='gym-list'),
# #     path('gyms/<int:pk>/', GymDetailView.as_view(), name='gym-detail'),
# #     path('rate-gym/', GymRatingView.as_view(), name='rate-gym'),
# # ]



# # myapp/urls.py
# from django.urls import path
# from .views import gym_list, gym_detail, gym_create, gym_update, gym_delete

# urlpatterns = [
#     path('gyms/', gym_list, name='gym_list'),
#     path('gyms/<int:pk>/', gym_detail, name='gym_detail'),
#     path('gyms/create/', gym_create, name='gym_create'),
#     path('gyms/<int:pk>/update/', gym_update, name='gym_update'),
#     path('gyms/<int:pk>/delete/', gym_delete, name='gym_delete'),
# ]


