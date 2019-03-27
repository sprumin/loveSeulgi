from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from gallery.utilities import pagination
from post.forms import NoticeCommentForm, PostCommentForm, ReportCommentForm
from post.models import Notice, Post, Report, NoticeComment, PostComment, ReportComment


# Create your views here.
def index(request):
    return HttpResponse("POST")


class NoticeView(View):
    def get(self, request, notice_id=None):
        if not request.user.is_authenticated:
            return redirect("/user/signin/")

        if notice_id:
            form = NoticeCommentForm
            notice = Notice.objects.get(id=notice_id)

            if not notice.user.is_superuser:
                return "This user is not admin"

            comment = NoticeComment.objects.filter(notice=notice)

            notice_data = {
                "id": notice.id,
                "title": notice.title,
                "content": notice.content,
                "views": notice.views,
                "comment": comment
            }

            if notice.photo:
                notice_data["photo"] = notice.photo

            # views update
            notice.views += 1
            notice.save()

            return render(request, "post/notice.html", {"notice": notice_data, "form": form})

        return render(request, "post/notice.html", {
            "notice": Notice.objects.all().order_by("-id")
        })

    def post(self, request, notice_id):
        pass


class PostView(View):
    def get(self, request, post_id=None):
        if not request.user.is_authenticated:
            return redirect("/user/signin/")

        if post_id:
            form = PostCommentForm
            post = Post.objects.get(id=post_id)
            comment = PostComment.objects.filter(post=post)

            post_data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "views": post.views,
                "thumbs": post.thumbs,
                "comment": comment
            }

            if post.photo:
                post_data["photo"] = post.photo

            # views update
            post.views += 1
            post.save()

            return render(request, "post/post.html", {"post": post_data, "form": form})

        return render(request, "post/post.html", {
            "post": Post.objects.all().order_by("-id")
        })

    def post(self, request, post_id):
        pass


class ReportView(View):
    def get(self, request, report_id=None):
        if not request.user.is_authenticated:
            return redirect("/user/signin/")

        if report_id:
            form = ReportCommentForm
            report = Report.objects.get(id=report_id)
            comment = ReportComment.objects.filter(report=report)

            report_data = {
                "id": report.id,
                "title": report.title,
                "category": report.category,
                "content": report.content,
                "views": report.views,
                "password": report.password,
                "status": report.status,
                "comment": comment
            }

            if report.photo:
                report["photo"] = report.photo

            # views update
            report.views += 1
            report.save()

            return render(request, "post/report.html", {"post": report_data, "form": form})

        return render(request, "post/report.html", {
            "report": Report.objects.all().order_by("-id")
        })

    def post(self, request, report_id):
        pass
