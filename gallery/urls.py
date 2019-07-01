from django.urls import path

from . import views


urlpatterns = [
    path("album/", views.AlbumView.as_view()),
    path("album/<int:photo_id>", views.AlbumView.as_view()),
    path("album/<str:is_gif>", views.AlbumView.as_view())
]
