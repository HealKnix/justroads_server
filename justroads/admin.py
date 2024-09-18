from django.contrib import admin

from justroads.models import Mark


# Register your models here.

class MarkAdmin(admin.ModelAdmin):
    model = Mark
    list_display = ['id']


admin.site.register(Mark, MarkAdmin)
