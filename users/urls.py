# gym_app/urls.py
from django.urls import path
from .views import UserSignUpView, UserLoginView, UpdateAgeView, UpdateLanguageView, UpdateLocationView


urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('api/update_age/', UpdateAgeView.as_view(), name='update_age'),
    path('api/update_location/', UpdateLocationView.as_view(), name='update_location'),
    path('api/update_language/', UpdateLanguageView.as_view(), name='update_language'),
]
#     path('club/edit_manager/', views.edit_manager, name='edit_manager'),