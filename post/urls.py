from django.urls import path

from . import views


urlpatterns = [
    path("", views.index),
    path("notice", views.NoticeView.as_view()),
    path("notice/<int:notice_id>", views.NoticeView.as_view()),
    path("post", views.PostView.as_view()),
    path("post/<int:post_id>", views.PostView.as_view()),
    path("report", views.ReportView.as_view()),
    path("report/<int:post_id>", views.ReportView.as_view())
]
