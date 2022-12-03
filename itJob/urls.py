from django.urls import path
from itJob import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("worker/<str:user_name>", views.worker_profile, name="worker_profile"),
    path("firm/<str:user_name>", views.firm_profile, name="firm_profile"),
    path("firm/<str:user_name>/create_work", views.create_work, name="create_work"),
    path("firm/<str:work_name>/edit_work", views.edit_work, name="edit_work"),
    # API
    path("profile/save_description", views.save_description, name="save_description"),
    path("profile/save_skills", views.save_skills, name="save_skills"),
    path("profile/save_photo", views.save_photo, name="save_photo"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
