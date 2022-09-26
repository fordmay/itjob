from ast import IsNot
import itertools
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from itJob.models import Firm, Worker, Worker_history_job, Worker_skill


def index(request):
    return render(request, "itJob/index.html")


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

        # Attempt to create new user
        try:
            if is_firm:
                user = Firm.objects.create_user(
                    username, email, password, is_firm=True)
            else:
                user = Worker.objects.create_user(username, email, password)
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
    if Worker.objects.filter(username=user_name).exists():
        return render(request, "itJob/worker_profile.html", {
            "worker": Worker.objects.get(username=user_name),
            "worker_skills": Worker_skill.objects.filter(worker__username=user_name),
            "worker_history_jobs": Worker_history_job.objects.filter(author__username=user_name)
        })
    else:
        return HttpResponseNotFound(f"<h1>User {user_name} not found</h1>")


def firm_profile(request, user_name):
    if Firm.objects.filter(username=user_name).exists():
        return render(request, "itJob/firm_profile.html", {
            "firm": Firm.objects.get(username=user_name)
        })
    else:
        return HttpResponseNotFound(f"<h1>User {user_name} not found</h1>")


@csrf_exempt
@login_required
def save_description(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if len(data) < 2000:
            user = Worker.objects.get(username=request.user)
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
                user = Worker.objects.get(username=request.user)
                Worker_skill(skill_name=new_skill["skill"], score=int(
                    new_skill["score"]), worker=user).save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)


@csrf_exempt
@login_required
def save_photo(request):
    if request.method == "POST":
        user = Worker.objects.get(username=request.user)
        new_first_name = request.POST.get("first_name").strip()
        new_last_name = request.POST.get("last_name").strip()
        new_image = request.FILES.get("avatar")
        if user.first_name != new_first_name or user.last_name != new_last_name:
            user.first_name = new_first_name
            user.last_name = new_last_name
            user.save()
        if user.image != new_image and new_image is not None:
            user.image = new_image
            user.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
