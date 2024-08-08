from rest_framework import serializers
from .models import LinkModel, UserLinkModel


class LinkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkModel
        fields = ('id', 'url')

