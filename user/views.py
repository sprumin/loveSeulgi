from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.views import View

from gallery.utilities import pagination
from user.forms import UserCreationForm, UserSignInForm, UserEditForm, UserDeleteForm
from user.models import User
from gallery.models import Album


# Create your views here.
def index(request):
    images = list()
    album = Album.objects.filter(is_gif=False).order_by("-id")

    for image in album:
        if len(images) > 20:
            break

        images.append(image.photo.url)

    return render(request, "index.html", {"images": images})


def about(request):
    return render(request, "about.html")


class UserSignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")

        form = UserCreationForm

        return render(request, "user/signup.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            try:
                User.objects.create_user(**form.cleaned_data)
            except ValueError:
                messages.error(request, "Password too short!")
            else:
                return redirect("/user/signin")

        return redirect("/user/signup")


class UserSignInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")

        form = UserSignInForm

        return render(request, "user/signin.html", {"form": form})

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)

            return redirect("/")

        messages.error(request, "Invalid email or password")

        return redirect("/user/signin")


class UserEditView(View):
    """ User information update """
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/user/signin")

        form = UserEditForm(initial={"email": request.user.email,
                                     "username": request.user.username})

        return render(request, "user/edit.html", {"form": form})

    def put(self, request):
        data = QueryDict(request.body)

        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        if password1 != password2 or len(password1) < 8:
            messages.error(request, "Password mismatch or Password too short")

            return HttpResponse(status=400)

        user = User.objects.get(email=request.user.email)

        user.username = username
        user.set_password(password1)

        user.save()

        return HttpResponse(status=200)


class UserDeleteView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/user/signin')

        form = UserDeleteForm

        return render(request, "user/delete.html", {"form": form})

    def post(self, request):
        email = request.POST.get("email")

        if request.user.email == email:
            user = User.objects.get(email=email)
            user.delete()

            return redirect("/")

        messages.error(request, "Does not match signed email")

        return redirect("/user/delete")


def signout(request):
    logout(request)

    return redirect("/")


class UserAlbumView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/user/signin")

        user = User.objects.get(email=request.user.email)
        user_album = list()

        photos = user.photos.all()

        if photos:
            for row in user.photos.all():
                user_album.append({
                    "id": row.id,
                    "title": row.title,
                    "photo": row.photo.url,
                    "source": row.source
                })

            return render(request, "user/album.html", pagination(request, user_album))
        else:
            messages.error(request, "The album does not have an image. Please add the picture first.")

            return redirect("/gallery/album")
