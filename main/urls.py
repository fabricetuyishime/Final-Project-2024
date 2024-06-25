from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("report", views.report, name="report"),
    path("train", views.train, name="train"),
    path("dataset", views.dataset, name="dataset"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("fish/", views.fish, name="fish"),
    path("fish/add", views.add_fish, name="add.fish"),
    path("harvest/", views.harvest, name="harvest"),
    path("harvest/add", views.add_harvest, name="add.harvest"),
    path("disease/", views.disease, name="disease"),
    path("disease/add", views.add_disease, name="add.disease"),
    path(
        "remove-image/<str:folder>/<str:img>/", views.delete_image, name="delete_image"
    ),
]
