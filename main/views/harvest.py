from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from ..models import Harvest


@require_http_methods(["GET"])
@login_required(login_url="signin")
def harvest(request):
    harvest = Harvest.objects.order_by("-id")
    paginator = Paginator(harvest, 20)
    page_number = request.GET.get("page")
    page_object = paginator.get_page(page_number)

    return render(request, "harvest/index.html", {"page_object": page_object})


@require_http_methods(["GET", "POST"])
@login_required(login_url="signin")
def add_harvest(request):
    if request.method == "GET":
        return render(request, "harvest/add.html")

    elif request.method == "POST":
        weight = request.POST["weight"]
        farmer = request.POST["farmer"]
        date = request.POST["date"]
        fish = request.POST["fish"]
        disease = request.POST["disease"]
        comment = request.POST["comment"]
        harvest = Harvest(
            weight=weight,
            date=date,
            fish=fish,
            disease=disease,
            farmer=farmer,
            comment=comment,
        )

        harvest.save()
        messages.info(request, "harvest saved")
        return redirect("harvest")
