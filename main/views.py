from django.contrib.auth import authenticate, login, logout as log_me_out
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Fish

# Create your views here.


@require_http_methods(["GET"])
def home(request):
    fish = Fish.objects.order_by("-id")
    paginator = Paginator(fish, 12)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "home.html", {"page_object": page_object})


@require_http_methods(["GET"])
@login_required(login_url="signin")
def dashboard(request):
    return render(request, "dashboard.html")


@require_http_methods(["GET"])
@login_required(login_url="signin")
def fish(request):
    fish = Fish.objects.order_by("-id")
    paginator = Paginator(fish, 20)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "fish/index.html", {"page_object": page_object})


@require_http_methods(["GET", "POST"])
@login_required(login_url="signin")
def add_fish(request):
    return render(request, "fish/add.html")


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    elif request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == "" or password != confirm_password:
            messages.info(request, "Password do not match")
            return redirect("signup")

        if email == "" or User.objects.filter(email=email).exists():
            messages.info(request, "Email already taken")
            return redirect("signup")

        if username == "" or User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect("signup")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()

        user_login = authenticate(username=username, password=password)
        login(request, user_login)

        user_model = User.objects.get(email=email)

        return redirect("dashboard")


@require_http_methods(["GET", "POST"])
def signin(request):
    if request.method == "GET":
        return render(request, "signin.html")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Invalid credentials")
            return redirect("signin")

        login(request, user)
        return redirect("dashboard")


@login_required(login_url="signin")
def logout(request):
    log_me_out(request)
    return redirect("home")
