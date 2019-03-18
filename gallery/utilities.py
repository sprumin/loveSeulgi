from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gallery.models import Album
from user.models import UserAlbum


def get_photos(request, user=None, photo_id=None, is_gif=None):
    photo_list = list()

    # get image
    if photo_id:
        return Album.objects.get(id=photo_id)

    # album photos list
    if user:
        for row in UserAlbum.objects.filter(user__email=user):
            photo_list.append({
                "id": row.id,
                "photo": row,
                "title": row.photo.title,
                "source": row.photo.source
            })
    else:
        if is_gif:
            condition = Album.objects.filter(is_gif=True)
        else:
            condition = Album.objects.filter(is_gif=False)

        for row in condition:
            photo_list.append({
                "id": row.id,
                "photo": row.photo.url,
                "title": row.title,
                "source": row.source
            })

    return pagination(request, photo_list)


def pagination(request, data_list):
    total_len = len(data_list)
    paginator = Paginator(data_list, 5)
    page = request.GET.get('page')

    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    index = photos.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0

    if index < 2:
        end_index = 5 - start_index
    else:
        end_index = index + 3 if index <= max_index - 3 else max_index

    page_range = list(paginator.page_range[start_index:end_index])

    return {"photos": photos, "page_range": page_range,
            "total_len": total_len, "max_index": max_index - 2}
