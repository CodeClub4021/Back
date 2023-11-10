from django.urls import path
from . import views
from .views import choose_view, choose_method

urlpatterns = [
    path('club/signup/', views.signup, name= 'signup'),
    path('club/login/', views.login_view, name= 'login'),
    path('club/loginsuc/', views.loginsuc, name='loginsuc'),
    path('club/choose/', choose_view, name='choose'),
    path('club/choose_method/', choose_method, name='choose_method'),

]