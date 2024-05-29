from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from ..models import Fish


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
