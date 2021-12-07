from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from .models import *


@admin.register(Group)
class AdminGroup(TranslationAdmin):
    fields = ('name', 'slug')


class PublicationAdminForm(forms.ModelForm):
    content_ru = forms.CharField(widget=TinyMCE)
    content_en = forms.CharField(widget=TinyMCE)

    class Meta:
        model = Publication
        fields = '__all__'


@admin.register(Publication)
class AdminPublication(admin.ModelAdmin):
    list_display = ('title', 'group', 'author',)

    class Media:
        js = [
            'tinymce/jquery.tinymce.min.js',
            'tinymce/tinymce.min.js',
            'tinymce/textareas.js'
        ]


admin.site.register(Tag)
admin.site.register(Rate)
