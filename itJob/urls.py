from django.urls import path
from itJob import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("worker/<str:user_name>", views.worker_profile, name="worker_profile"),
    path("firm/<str:user_name>", views.firm_profile, name="firm_profile"),

    path("profile/save_description", views.save_description, name="save_description"),
]
