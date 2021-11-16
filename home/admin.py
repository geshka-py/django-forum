from django.contrib import admin
from .models import Group, Publication

admin.site.register(Group)


@admin.register(Publication)
class AdminPublication(admin.ModelAdmin):
    list_display = ('title', 'group', 'author')
