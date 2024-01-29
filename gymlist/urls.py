from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from gymlist import views


urlpatterns = [
    path('gyms/', views.GymList.as_view()),
    path('managers/', views.ManagerList.as_view()),
    path('gyms/<int:pk>/', views.GymDetail.as_view()),
    path('register/', views.RegistrationView.as_view()),
    path('login/', obtain_auth_token),
    path('user/', views.CurrentUser.as_view()),
    path('customer/join-gym/', views.CustomerJoinGymView.as_view()),
    path('customer/joined-gyms/', views.CustomerJoinedGymsView.as_view()),
    path('coach/join-gym/', views.CoachJoinGymView.as_view()),
    path('coach/joined-gyms/', views.CoachJoinedGymsView.as_view()),
    path('customer/update/', views.CustomerUpdateView.as_view()),
    path('manager/update/', views.ManagerUpdateView.as_view()),
    path('coach/update/', views.CoachUpdateView.as_view()),
    path('change-password/', views.PasswordChangeView.as_view()),
    path('customer/rate-gym/', views.GymRatingCreateView.as_view()),
    path('customer/rate-coach', views.CoachRatingCreateView.as_view()),
    path('manager/list-coaches', views.CompletedInfoCoachListView.as_view()),
    path('gym/<int:pk>/add-coach/', views.AddCoachToGymView.as_view()),
]



urlpatterns = format_suffix_patterns(urlpatterns)