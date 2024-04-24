from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("logout", views.logout, name="logout"),
    # path("article/", views.ArticleList.as_view(), name="articles"),
    # path("article/<slug:slug>", views.ArticleDetail.as_view(), name="article"),
    # path("category/<slug:slug>", views.CategoryDetail.as_view(), name="category"),
    # path("page/<slug:slug>", views.PageDetail.as_view(), name="page"),
]
