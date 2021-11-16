from django import forms
from .models import Publication, Rate, Comment


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title', 'description', 'group', 'content')


class RateIt(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ('rate',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)
