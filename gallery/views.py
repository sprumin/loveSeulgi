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

        if photo_id:
            form = AlbumCommentForm
            photo = Album.objects.get(id=photo_id)
            comment = AlbumComment.objects.filter(photo=photo)

            photo_data = {
                "id": photo.id,
                "photo": photo.photo.url,
                "title": photo.title,
                "source": photo.source,
                "comment": comment
            }
            return render(request, "gallery/album.html", {"photo": photo_data, "form": form})

        return render(request, "gallery/album.html", get_photos(request))

    def post(self, request, photo_id=None):
        username = request.POST.get("username", None)
        comment = request.POST.get("comment", None)

        if username and comment:
            photo = Album.objects.get(id=photo_id)

            album_com = AlbumComment(photo=photo, username=username, message=comment)
            album_com.save()

            return redirect(f"/gallery/album/{photo_id}")