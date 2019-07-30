from django.urls import path
from . import views


urlpatterns = [
    path("signup", views.UserSignUpView.as_view()),
    path("signin", views.UserSignInView.as_view()),
    path("edit", views.UserEditView.as_view()),
    # path("album?$", views.UserAlbumView.as_view()),
    path("signout", views.signout),
]