from django.contrib import admin
from .models import Group, Publication, UserPublicationRelation

admin.site.register(Group)


@admin.register(Publication)
class AdminPublication(admin.ModelAdmin):
    list_display = ('title', 'group', 'author')


@admin.register(UserPublicationRelation)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'publication', 'rate', 'published')
