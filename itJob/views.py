import itertools
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from itJob.models import *


def index(request):
    return render(request, "itJob/index.html", {
        "firm_works": pagination(request, 10, Firm_work.objects.filter(active=True).order_by("time").reverse()),
        "firm_work_skills": Firm_work_skill.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "itJob/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "itJob/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        is_firm = request.POST.get("checkbox", False)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "itJob/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user and check firm
        try:
            user = User.objects.create_user(
                username, email, password, is_firm=True if is_firm else False)
            user.save()
        except IntegrityError:
            return render(request, "itJob/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "itJob/register.html")


def worker_profile(request, user_name):
    if User.objects.filter(username=user_name).exists():
        return render(request, "itJob/worker_profile.html", {
            "worker": User.objects.get(username=user_name),
            "worker_skills": Worker_skill.objects.filter(worker__username=user_name),
            "worker_history_jobs": Worker_history_job.objects.filter(author__username=user_name)
        })
    else:
        return HttpResponseNotFound(f"<h1>User {user_name} not found</h1>")


def firm_profile(request, user_name):
    if User.objects.filter(username=user_name).exists():
        return render(request, "itJob/firm_profile.html", {
            "firm": User.objects.get(username=user_name),
            "firm_works": pagination(request, 5, Firm_work.objects.filter(author__username=user_name).order_by("time").reverse()),
            "firm_work_skills": Firm_work_skill.objects.filter(work__author__username=user_name)
        })
    else:
        return HttpResponseNotFound(f"<h1>User {user_name} not found</h1>")


def pagination(request, number_posts, objects):
    paginator = Paginator(objects, number_posts)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj

def create_work(request, user_name):
    if request.user.username == user_name and User.objects.filter(username=user_name, is_firm=True).exists():
        return render(request, "itJob/work_profile.html")
    else:
        return HttpResponseNotFound(f"<h1>You are not user {user_name} or you not firm</h1>")

def edit_work(request, work_name):
    
    return render(request, "itJob/work_profile.html")


# API
@csrf_exempt
@login_required
def save_description(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if len(data) < 2000:
            user = User.objects.get(username=request.user)
            # Check changes before save
            if user.description != data:
                user.description = data
                user.save()
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@csrf_exempt
@login_required
def save_skills(request):
    if request.method == "POST":
        new_skills = json.loads(request.body)
        user_skills = Worker_skill.objects.filter(worker=request.user)
        for new_skill, user_skill in itertools.zip_longest(new_skills, user_skills):
            if new_skill is not None and user_skill is not None:
                # Check changes before save
                if user_skill.skill_name != new_skill["skill"] or user_skill.score != int(new_skill["score"]):
                    user_skill.skill_name = new_skill["skill"]
                    user_skill.score = int(new_skill["score"])
                    user_skill.save()
            if new_skill is None:
                user_skill.delete()
            if user_skill is None:
                user = User.objects.get(username=request.user)
                Worker_skill(skill_name=new_skill["skill"], score=int(
                    new_skill["score"]), worker=user).save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@csrf_exempt
@login_required
def save_photo(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        # Save image
        new_image = request.FILES.get("avatar")
        if user.image != new_image and new_image is not None:
            user.image = new_image
            user.save()
        # Save first name and last name if user isn't firm
        if not user.is_firm:
            new_first_name = request.POST.get("first_name").strip()
            new_last_name = request.POST.get("last_name").strip()
            if user.first_name != new_first_name or user.last_name != new_last_name:
                user.first_name = new_first_name
                user.last_name = new_last_name
                user.save()
        # Save firm name if user is firm
        if user.is_firm:
            new_firm_name = request.POST.get("firm_name").strip()
            if user.firm_name != new_firm_name:
                user.firm_name = new_firm_name
                user.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
