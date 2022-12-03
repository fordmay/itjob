from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    is_firm = models.BooleanField(default=False)
    firm_name = models.CharField(max_length=64, blank=True)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(max_length=2000, blank=True)


SCORES = [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
]


class Worker_skill(models.Model):
    skill_name = models.CharField(max_length=64)
    score = models.IntegerField(default=0, choices=SCORES)
    worker = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"id:{self.pk}, skill:{self.skill_name}, score:{self.score}, worker:{self.worker}"


class Worker_history_job(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    firm = models.CharField(max_length=64)
    description = models.TextField(max_length=2000)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class Firm_work(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    work_title = models.CharField(max_length=64)
    salary = models.DecimalField(max_digits=9, decimal_places=0, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Firm_work_skill(models.Model):
    skill_name = models.CharField(max_length=64)
    score = models.IntegerField(default=0, choices=SCORES)
    work = models.ForeignKey(Firm_work, on_delete=models.CASCADE)

    def __str__(self):
        return f"id:{self.pk}, skill:{self.skill_name}, score:{self.score}, work:{self.work}"
