from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Firm_work)
admin.site.register(Worker_history_job)
admin.site.register(Worker_skill)
admin.site.register(Firm_work_skill)