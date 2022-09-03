from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    is_firm = models.BooleanField(default=False)
    image = models.URLField(blank=True)
    description = models.TextField(max_length=2000, blank=True)
    
class Worker(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, parent_link=True)

    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

class Worker_skill(models.Model):
    SCORES = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    skill_name = models.CharField(max_length=64)
    score = models.IntegerField(default=0, choices=SCORES)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

    def __str__(self):
        return f"id:{self.pk}, skill:{self.skill_name}, score:{self.score}, worker:{self.worker}"

class Worker_history_job(models.Model):
    author = models.ForeignKey(Worker, on_delete=models.CASCADE)
    firm = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

class Firm(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, parent_link=True)
    name = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = 'Firm'
        verbose_name_plural = 'Firms'

class Firm_work(models.Model):
    author = models.ForeignKey(Firm, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField(max_length=600)
    time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
