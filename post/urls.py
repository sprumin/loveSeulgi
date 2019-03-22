from django.urls import path

from . import views


urlpatterns = [
    path("", views.index),
    path("post", views.PostView.as_view()),
    path("post/<int:post_id>", views.PostView.as_view()),
]
