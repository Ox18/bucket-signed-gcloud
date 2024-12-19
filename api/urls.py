from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('pre-upload', views.signedUrl, name='signedUrl'),
    path('verify', views.verify, name='verify'),
]