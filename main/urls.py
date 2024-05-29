from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    path("report", views.report, name="report"),
    path("dataset", views.dataset, name="dataset"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("fish/", views.fish, name="fish"),
    path("fish/add", views.add_fish, name="add.fish"),
    path("harvest/", views.harvest, name="harvest"),
    path("harvest/add", views.add_harvest, name="add.harvest"),
    path("disease/", views.disease, name="disease"),
    path("disease/add", views.add_disease, name="add.disease"),
]
