from django import forms
from .models import UserPublicationRelation


class UserPublicationRelationForm(forms.ModelForm):
    class Meta:
        model = UserPublicationRelation
        fields = ('rate', 'comment')

    def save(self, commit=True):
        relation = super(UserPublicationRelationForm, self).save(commit=False)
        if commit:
            relation.save()
        return relation
