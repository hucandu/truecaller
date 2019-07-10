from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register),
    path('user_login/', views.token),
    path('user_logout/', views.logout),
]
