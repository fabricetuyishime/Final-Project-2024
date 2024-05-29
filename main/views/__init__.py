import os, random
from .fish import *
from .disease import *
from .harvest import *
from .authenticate import *
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from ..models import Disease, Fish, Harvest
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from ..prediction.identify import identify_image
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


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
    generate_data()
    harvest = Harvest.objects.order_by("-id")
    paginator = Paginator(harvest, 50)
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


def generate_data():
    fish_list = list(Fish.objects.all())
    disease_list = list(Disease.objects.all())

    farmer_list = [
        "Alice",
        "Bob",
        "Charlie",
        "Diana",
        "Ethan",
        "Fiona",
        "George",
        "Hannah",
        "Ian",
        "Jasmine",
    ]

    comment_list = [
        "Great catch today!",
        "Quality looks good.",
        "Smaller fish than usual.",
        "Biggest haul this season!",
        "Need to check for diseases.",
        "Perfect size for market.",
        "Healthy and vibrant fish.",
        "Low yield, need more feed.",
        "Excellent color and texture.",
        "More variety in this batch.",
    ]

    for i in range(100):
        fish = random.choice(fish_list)
        farmer = random.choice(farmer_list)
        comment = random.choice(comment_list)
        weight = round(random.uniform(10.0, 100.0), 2)
        created_at = datetime(2024, random.randint(1, 5), random.randint(1, 29))
        disease = random.choice(disease_list) if random.choice([True, False]) else None

        harvest = Harvest(
            weight=weight,
            farmer=farmer,
            comment=comment,
            fish=fish,
            disease=disease,
            date=created_at.date(),
        )

        harvest.save()