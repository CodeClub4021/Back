from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token
from gymlist import views


urlpatterns = [
    path('gyms/', views.GymList.as_view()),
    path('gyms/<int:pk>/', views.GymDetail.as_view()),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)