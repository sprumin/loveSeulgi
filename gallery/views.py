from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from gallery.forms import AlbumCommentForm
from gallery.utilities import pagination
from gallery.models import Album, AlbumComment
from user.models import User


# Create your views here.
def index(request):
    return HttpResponse("GALLERY")


class AlbumView(View):
    def get(self, request, photo_id=None):
        if not request.user.is_authenticated:
            return redirect("/user/signin/")

        is_gif = request.POST.get("is_gif", None)

        # send photo data
        if photo_id:
            form = AlbumCommentForm
            photo = Album.objects.get(id=photo_id)
            comment = AlbumComment.objects.filter(photo=photo)

            photo_data = {
                "id": photo.id,
                "photo": photo.photo.url,
                "title": photo.title,
                "source": photo.source,
                "views": photo.views,
                "thumbs": photo.thumbs,
                "comment": comment
            }

            # update views
            photo.views += 1
            photo.save()

            return render(request, "gallery/album.html", {"photo": photo_data, "form": form})

        if is_gif:
            condition = Album.objects.filter(is_gif=True).order_by("-id")
        else:
            condition = Album.objects.filter(is_gif=False).order_by("-id")

        photo_list = list()

        for row in condition:
            photo_list.append({
                "id": row.id,
                "photo": row.photo.url,
                "title": row.title,
                "source": row.source,
                "comments": len(AlbumComment.objects.filter(photo=row))
            })

        return render(request, "gallery/album.html", pagination(request, photo_list))

    def post(self, request, photo_id):
        photo = Album.objects.get(id=photo_id)

        username = request.POST.get("username", None)
        comment = request.POST.get("comment", None)
        thumbs = request.POST.get("thumbs", None)
        myalbum = request.POST.get("myalbum", None)

        # save photo comment
        if username and comment:
            album_com = AlbumComment(photo=photo, username=username, message=comment)
            album_com.save()

        # update thumbs
        # TODO: 일단 횟수제한 없이 세팅하고 프로젝트 완료시 redis에 횟수제한걸기
        if thumbs:
            photo.thumbs += 1
            # thumbs 데이터를 view 로 전송할 때 해당 url에 접근하기때문에 조회수가 두번 누적되어서 한번 빼준다
            photo.views -= 1
            photo.save()

        # UserAlbum 에 해당 photo 등록시키기
        if myalbum:
            user = User.objects.get(email=request.user.email)

            if photo in user.photos.all():
                return HttpResponse(status=400)
            else:
                # ManyToManyField 라서 add 로 추가해줘야함
                user.photos.add(photo)
                user.save()

        return redirect(f"/gallery/album/{photo_id}")