from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from gallery.utilities import pagination
from user.models import User
from post.forms import NoticeAddForm, PostAddForm, ReportAddForm, NoticeCommentForm, PostCommentForm, ReportCommentForm
from post.models import Notice, Post, Report, NoticeComment, PostComment, ReportComment


# Create your views here.
class NoticeView(View):
    def get(self, request, notice_id=None):
        if notice_id:
            form = NoticeCommentForm
            notice = Notice.objects.get(id=notice_id)

            if not notice.user.is_superuser:
                return HttpResponse("This user is not admin")

            comments = NoticeComment.objects.filter(notice=notice)

            # views update
            notice.views += 1
            notice.save()

            notice_data = {
                "id": notice.id,
                "title": notice.title,
                "content": notice.content,
                "views": notice.views,
            }

            if comments:
                notice_data["comments"] = pagination(request, comments, 5)

            if notice.photo:
                notice_data["photo"] = notice.photo.url

            return render(request, "post/notice.html", {"notice": notice_data, "form": form})
        else:
            if request.user.is_authenticated:
                form = NoticeAddForm(initial={"user": User.objects.get(email=request.user.email)})
            else:
                form = "Anonymous User"

            notice_list = list()

            for row in Notice.objects.all().order_by("-id"):
                notice_list.append({
                    "id": row.id,
                    "title": row.title,
                    "content": row.content,
                    "views": row.views,
                    "comments": len(NoticeComment.objects.filter(notice=row))
                })

            return render(request, "post/notice.html", {
                "pagination": pagination(request, notice_list, 10),
                "form": form
            })

    def post(self, request, notice_id=None):
        if notice_id:
            notice = Notice.objects.get(id=notice_id)

        username = request.POST.get("username", None)
        comment = request.POST.get("comment", None)

        if username and comment:
            notice_com = NoticeComment(notice=notice, username=username, message=comment)
            notice_com.save()
        else:
            user = User.objects.get(email=request.user.email)

            if not user.is_superuser:
                return HttpResponse("User is not admin")

            title = request.POST.get("title", None)
            photo = request.FILES.get("photo", None)
            content = request.POST.get("content", None)

            if title and content:
                notice = Notice(user=user, title=title, photo=photo, content=content)
                notice.save()

            return redirect("/post/notice")

        return redirect(f"/post/notice/{notice_id}")


class PostView(View):
    def get(self, request, post_id=None):
        if post_id:
            form = PostCommentForm
            post = Post.objects.get(id=post_id)
            comments = PostComment.objects.filter(post=post)

            # views update
            post.views += 1
            post.save()

            post_data = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "views": post.views,
                "thumbs": post.thumbs,
            }

            if comments:
                post_data["comments"] = pagination(request, comments, 5)

            if post.photo:
                post_data["photo"] = post.photo.url

            return render(request, "post/post.html", {"post": post_data, "form": form})
        else:
            if request.user.is_authenticated:
                form = PostAddForm(initial={"user": request.user.email})
            else:
                form = "Anonymous User"

            post_list = list()

            for row in Post.objects.all().order_by("-id"):
                post_list.append({
                    "id": row.id,
                    "title": row.title,
                    "content": row.content,
                    "views": row.views,
                    "comments": len(PostComment.objects.filter(post=row))
                })

            return render(request, "post/post.html", {
                "pagination": pagination(request, post_list, 10),
                "form": form
            })

    def post(self, request, post_id=None):
        if post_id:
            post = Post.objects.get(id=post_id)

        username = request.POST.get("username", None)
        comment = request.POST.get("comment", None)
        thumbs = request.POST.get("thumbs", None)

        if username and comment:
            post_com = PostComment(post=post, username=username, message=comment)
            post_com.save()
        elif thumbs:
            post.thumbs += 1
            post.views -= 1
            post.save()
        else:
            user = User.objects.get(email=request.user.email)
            title = request.POST.get("title", None)
            photo = request.FILES.get("photo", None)
            content = request.POST.get("content", None)

            if title and content:
                try:
                    post = Post(user=user, title=title, photo=photo, content=content)
                    post.save()
                except ValueError:
                    return HttpResponse("Invalid Photo")

            return redirect("/post/post")

        return redirect(f"/post/post/{post_id}")

    def delete(self, request, post_id=None):
        if post_id:
            post = Post.objects.get(id=post_id)
            post.delete()
            
            return HttpResponse(status=200)

        return HttpResponse(status=400)


class ReportView(View):
    def get(self, request, report_id=None):
        if report_id:
            form = ReportCommentForm
            report = Report.objects.get(id=report_id)
            comments = ReportComment.objects.filter(report=report)

            # views update
            report.views += 1
            report.save()

            report_data = {
                "id": report.id,
                "title": report.title,
                "category": report.category,
                "content": report.content,
                "views": report.views,
                "password": report.password,
                "status": report.status,
            }

            if comments:
                report_data["comments"] = pagination(request, comments, 5)

            if report.photo:
                report_data["photo"] = report.photo.url

            return render(request, "post/report.html", {"report": report_data, "form": form})
        else:
            if request.user.is_authenticated:
                form = ReportAddForm(initial={"user": request.user.email})
            else:
                form = "Anonymous User"

            report_list = list()

            for row in Report.objects.all().order_by("-id"):
                report_list.append({
                    "id": row.id,
                    "category": row.category,
                    "title": row.title,
                    "content": row.content,
                    "views": row.views,
                    "comments": len(ReportComment.objects.filter(report=row)),
                    "password": True if row.password else False
                })

            return render(request, "post/report.html", {
                "pagination": pagination(request, report_list, 10),
                "form": form
            })

    def post(self, request, report_id=None):
        if report_id:
            report = Report.objects.get(id=report_id)

        username = request.POST.get("username", None)
        comment = request.POST.get("comment", None)
        post_pw = request.POST.get("post_pw", None)

        if username and comment:
            report_com = ReportComment(report=report, username=username, message=comment)
            report_com.save()
        elif post_pw:
            report = Report.objects.get(id=report_id)

            if report.password == post_pw:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=400)
        else:
            user = User.objects.get(email=request.user.email)
            category = request.POST.get("category", None)
            title = request.POST.get("title", None)
            photo = request.FILES.get("photo", None)
            content = request.POST.get("content", None)
            password = request.POST.get("password", None)

            if category and title and content:
                try:
                    report = Report(user=user, category=category, title=title, photo=photo,
                                    content=content, password=password)
                    report.save()
                except ValueError:
                    return HttpResponse("Invalid Photo")

            return redirect("/post/report")

        return redirect(f"/post/report/{report_id}")

    def delete(self, request, report_id=None):
        if report_id:
            report = Report.objects.get(id=report_id)
            report.delete()
            
            return HttpResponse(status=200)

        return HttpResponse(status=400)
