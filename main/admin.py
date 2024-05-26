from django.contrib import admin
from .models import Fish, Disease, Harvest

# Register your models here.
admin.site.register(Fish)
admin.site.register(Disease)
admin.site.register(Harvest)
