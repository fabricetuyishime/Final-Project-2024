from datetime import datetime
import os, random
from django.conf import settings
from django.contrib.auth import authenticate, login, logout as log_me_out
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Disease, Fish, Harvest
from .prediction.identify import identify_image

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
def report(request):
    harvest = Harvest.objects.order_by("-id")
    paginator = Paginator(harvest, 20)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "report.html", {"page_object": page_object})


@require_http_methods(["GET", "POST"])
@login_required(login_url="signin")
def dataset(request):
    if request.method == "GET":
        sick_path = os.path.join(settings.MEDIA_ROOT, "dataset/sick")
        healthy_path = os.path.join(settings.MEDIA_ROOT, "dataset/healthy")

        sick_images = [
            f
            for f in os.listdir(sick_path)
            if os.path.isfile(os.path.join(sick_path, f))
        ]
        healthy_images = [
            f
            for f in os.listdir(healthy_path)
            if os.path.isfile(os.path.join(healthy_path, f))
        ]

        context = {"sick_images": sick_images, "healthy_images": healthy_images}
        return render(request, "dataset.html", context)

    elif request.method == "POST":
        if request.FILES.get("image") != None:
            image = request.FILES["image"]
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)

            with open(image_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            result = identify_image(image_path)
            messages.info(request, result)

        return redirect("dataset")


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
    if request.method == "GET":
        return render(request, "fish/add.html")

    elif request.method == "POST":
        age = request.POST["age"]
        name = request.POST["name"]
        size = request.POST["size"]
        description = request.POST["description"]
        fish = Fish(
            age=age,
            size=size,
            name=name,
            description=description,
        )

        if request.FILES.get("image") != None:
            fish.image = request.FILES.get("image")

        fish.save()
        messages.info(request, "fish saved")
        return redirect("fish")


@require_http_methods(["GET"])
@login_required(login_url="signin")
def disease(request):
    diseases = Disease.objects.order_by("-id")
    paginator = Paginator(diseases, 20)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "disease/index.html", {"page_object": page_object})


@require_http_methods(["GET", "POST"])
@login_required(login_url="signin")
def add_disease(request):
    if request.method == "GET":
        return render(request, "disease/add.html")

    elif request.method == "POST":
        name = request.POST["name"]
        symptom = request.POST["symptom"]
        treatment = request.POST["treatment"]
        description = request.POST["description"]

        disease = Disease(
            name=name,
            symptom=symptom,
            treatment=treatment,
            description=description,
        )

        disease.save()
        messages.info(request, "disease saved")
        return redirect("disease")


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


def generate_data():
    fish_list = list(Fish.objects.all())
    disease_list = list(Disease.objects.all())

    for i in range(100):
        weight = round(random.uniform(1.0, 10.0), 2)
        farmer = f"Farmer {i+1}"
        comment = f"This is a sample comment for harvest {i+1}."
        fish_id = random.choice(fish_list)
        disease_id = (
            random.choice(disease_list) if random.choice([True, False]) else None
        )
        created_at = datetime.now()

        harvest = Harvest(
            weight=weight,
            farmer=farmer,
            comment=comment,
            fish_id=fish_id,
            disease_id=disease_id,
            created_at=created_at,
        )

        harvest.save()
