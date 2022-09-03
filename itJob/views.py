from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
                user = Firm.objects.create_user(username, email, password, is_firm=True)
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

def worker_profile (request, user_name):
    if Worker.objects.filter(username=user_name).exists():
        return render(request, "itJob/worker_profile.html", {
            "worker": Worker.objects.get(username=user_name),
            "worker_skills": Worker_skill.objects.filter(worker__username=user_name),
            "all_scores": Worker_skill.SCORES,
            "worker_history_jobs": Worker_history_job.objects.filter(author__username=user_name)
        })
    else:
        return HttpResponseNotFound(f"<h1>User {user_name} not found</h1>")

def firm_profile (request, user_name):
    if Firm.objects.filter(username=user_name).exists():
        return render(request, "itJob/firm_profile.html", {
            "firm_info": Firm.objects.get(username=user_name)
        })
    else:
        return HttpResponseNotFound(f"<h1>User {user_name} not found</h1>")

@login_required
def save_description (request):
    if request.method == "POST":
        print(request.user)
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=400)