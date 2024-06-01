from django.contrib import admin
from .models import Fish, Disease, Harvest


class HarvestAdmin(admin.ModelAdmin):
    list_display = ("farmer", "weight", "date", "fish", "disease", "created_at")
    search_fields = ("farmer", "comment", "fish__name", "disease__name")
    list_filter = ("date", "fish", "disease", "farmer")

    ordering = ("-date",)
    date_hierarchy = "date"


admin.site.register(Harvest, HarvestAdmin)
admin.site.register(Fish)
admin.site.register(Disease)
