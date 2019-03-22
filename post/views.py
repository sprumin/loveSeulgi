from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from post.models import Post, PostComment


# Create your views here.
def index(request):
    return HttpResponse("POST")


class PostView(View):
    def get(self, request, post_id=None):
        if not request.user.is_authenticated:
            return redirect("/user/signin/")

        if post_id:
            pass

        return render(request, "post/post.html", {
            "notice": Post.objects.filter(category="NOTICE").order_by("-id"),
            "post": Post.objects.filter(category="POST").order_by("-id")
        })

    def post(self, request, post_id):
        pass
