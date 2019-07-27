from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from gallery.forms import AlbumCommentForm
from gallery.utilities import pagination
from gallery.models import Album, AlbumComment
from user.models import User


# Create your views here.
class AlbumView(View):
    def get(self, request, photo_id=None, is_gif=None):
        # send photo data
        if photo_id:
            form = AlbumCommentForm

            try:
                photo = Album.objects.get(id=photo_id)
            except:
                messages.error(request, "Invalid photo id")

                return redirect("/gallery/album")

            comments = AlbumComment.objects.filter(photo=photo)

            # update views
            photo.views += 1
            photo.save()

            photo_data = {
                "id": photo.id,
                "photo": photo.photo.url,
                "title": photo.title.replace("\\", ""),
                "source": photo.source,
                "views": photo.views,
                "thumbs": photo.thumbs,
            }

            if comments:
                photo_data["comments"] = pagination(request, comments, 5)

            return render(request, "gallery/album.html", {"photo": photo_data, "form": form})

        if is_gif:
            if is_gif == "gif":
                condition = Album.objects.filter(is_gif=True).order_by("-id")
            else:
                return redirect("/gallery/album/")
        else:
            condition = Album.objects.filter(is_gif=False).order_by("-id")

        photo_list = list()

        for row in condition:
            photo_list.append({
                "id": row.id,
                "photo": row.photo.url,
                "title": row.title.replace("\\", ""),
                "source": row.source,
                "upload_time": row.created_at,
                "views": row.views,
                "thumbs": row.thumbs,
                "comments": len(AlbumComment.objects.filter(photo=row))
            })

        return render(request, "gallery/album.html", pagination(request, photo_list, 10))

    def post(self, request, photo_id):
        photo = Album.objects.get(id=photo_id)

        username = request.POST.get("username", None)
        comment = request.POST.get("comment", None)
        thumbs = request.POST.get("thumbs", None)
        add_myalbum = request.POST.get("add_myalbum", None)
        del_myalbum = request.POST.get("del_myalbum", None)

        # save photo comment
        if username and comment:
            album_com = AlbumComment(photo=photo, username=username, message=comment)
            album_com.save()

        # update thumbs
        # TODO: 일단 횟수제한 없이 세팅하고 프로젝트 완료시 redis에 횟수제한걸기
        if thumbs:
            
            user = User.objects.get(email=request.user.email)

            if user not in photo.thumbers.all():
                photo.thumbs += 1
                photo.thumbers.add(user)
                # thumbs 데이터를 view 로 전송할 때 해당 url에 접근하기때문에 조회수가 두번 누적되어서 한번 빼준다
                photo.views -= 1
                photo.save()

                messages.info(request, "Thumb is complete!")
            else:
                photo.thumbs -= 1
                photo.thumbers.remove(user)
                photo.views -= 1
                photo.save()
                messages.error(request, "Thumb is cancel!")
        """
        # UserAlbum 에 해당 photo 등록/삭제 시키기
        if add_myalbum:
            user = User.objects.get(email=request.user.email)
            if photo in user.photos.all():
                messages.error(request, "Photo already registered.")

                return HttpResponse(status=400)
            else:
                user.photos.add(photo)
                user.save()

                messages.info(request, "Photo add is complete!")

        elif del_myalbum:
            user = User.objects.get(email=request.user.email)
            if photo not in user.photos.all():
                messages.error(request, "This is Photo that is not in the album.")

                return HttpResponse(status=400)
            else:
                user.photos.remove(photo)
                user.save()

                messages.info(request, "Photo delete is complete!")

        return HttpResponse(status=200)
        """