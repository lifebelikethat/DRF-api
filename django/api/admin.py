from django.contrib import admin
import api
from . import models
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

# Register your models here.
app = apps.get_app_config("api").get_models()

@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("book", "page",)
    ordering = ("page",)

for model in app:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
