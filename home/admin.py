from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *


@admin.register(Group)
class AdminGroup(TranslationAdmin):
    fields = ('name', 'slug')


class PublicationAdminForm(forms.ModelForm):
    content_ru = forms.CharField(widget=CKEditorWidget())
    content_en = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Publication
        fields = '__all__'


@admin.register(Publication)
class AdminPublication(TranslationAdmin):
    list_display = ('title', 'group', 'author',)


admin.site.register(Tag)
