from django.urls import path
from .views import GymListCreateView, GymDetailView, RatingCreateView, RatingListView

urlpatterns = [
    path('gyms/', GymListCreateView.as_view(), name='gym-list-create'),
    path('gyms/<int:pk>/', GymDetailView.as_view(), name='gym-detail'),
    path('gyms/<int:pk>/ratings/', RatingCreateView.as_view(), name='rating-create'),
    path('ratings/', RatingListView.as_view(), name='rating-list'),
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


