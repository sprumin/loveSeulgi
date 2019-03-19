from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from gallery.utilities import get_photos
from gallery.models import Album


# Create your views here.
def index(request):
    return HttpResponse("GALLERY")


class AlbumView(View):
    def get(self, request, photo_id=None):
        if not request.user.is_authenticated:
            return redirect("/user/signin/")

        if photo_id:
            return render(request, "gallery/photo.html", Album.objects.get(id=photo_id))

        return render(request, "gallery/album.html", get_photos(request))
