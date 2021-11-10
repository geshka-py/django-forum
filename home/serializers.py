from rest_framework import serializers
from .models import UserPublicationRelation


class UserPublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPublicationRelation
        fields = ('publication', 'rate', 'like')
