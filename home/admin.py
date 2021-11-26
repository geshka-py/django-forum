from django.contrib import admin

from .models import Group, Publication, Tag

admin.site.register(Group)
admin.site.register(Tag)


@admin.register(Publication)
class AdminPublication(admin.ModelAdmin):
    list_display = ('title', 'group', 'author')
