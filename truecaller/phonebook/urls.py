from django.urls import path

from phonebook.v1 import views

urlpatterns = [
    path('search/', views.SearchView.as_view()),
    path('mark_spam/',views.MarkSpamView.as_view())
]
