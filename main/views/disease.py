from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from ..models import Disease


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
