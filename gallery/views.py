from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from gallery.forms import AlbumCommentForm
from gallery.utilities import get_photos
from gallery.models import Album, AlbumComment


# Create your views here.
def index(request):
    return HttpResponse("GALLERY")


class AlbumView(View):
    def get(self, request, photo_id=None):
        if not request.user.is_authenticated:
            return redirect("/user/signin/")

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

        return render(request, "gallery/album.html", get_photos(request))

    def post(self, request, photo_id):
        photo = Album.objects.get(id=photo_id)

        username = request.POST.get("username", None)
        comment = request.POST.get("comment", None)
        thumbs = request.POST.get("thumbs", None)

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

        return redirect(f"/gallery/album/{photo_id}")