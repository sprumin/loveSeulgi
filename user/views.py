from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import UserCreationForm, UserSignInForm, UserDeleteForm
from .models import User


# Create your views here.
def user_info(request):
    if not request.user.is_authenticated:
        return redirect("/user/signin/")

    return HttpResponse("User")


class UserSignUpView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/user/")

        form = UserCreationForm

        return render(request, "user/signup.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)

            return redirect("/user/signin/")

        return HttpResponse("Form is invalid")


class UserSignInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/user/")

        form = UserSignInForm

        return render(request, "user/signin.html", {"form": form})

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)

            return redirect("/user/")

        return HttpResponse("Invalid email or password")


class UserDeleteView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/user/signin/')

        form = UserDeleteForm

        return render(request, "user/delete.html", {"form": form})

    def post(self, request):
        email = request.POST.get("email")

        if request.user.email == email:
            user = User.objects.get(email=email)
            user.delete()

            return redirect("/user/")

        return HttpResponse("Does not match signed email")


def signout(request):
    logout(request)

    return redirect("/user/")
