from django.urls import path

from .views import UserLoginView, UserView

urlpatterns = [
    path("accounts/", UserView.as_view()),
    path("accounts/newest/<int:num>/", UserView.as_view()),
    path("login/", UserLoginView.as_view()),
]
