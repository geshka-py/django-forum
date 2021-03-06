from django import forms
from tinymce.widgets import TinyMCE

from .models import Publication, Rate, Comment


class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ('title', 'content', 'group', 'tags',)


class RateIt(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('rate',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

