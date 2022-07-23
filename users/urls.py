from django.urls import path

from .views import UserDetailView, UserLoginView, UserView

urlpatterns = [
    path("accounts/", UserView.as_view()),
    path("accounts/<pk>/", UserDetailView.as_view()),
    path("accounts/<pk>/management/", UserDetailView.as_view()),
    path("accounts/newest/<int:num>/", UserView.as_view()),
    path("login/", UserLoginView.as_view()),
]
