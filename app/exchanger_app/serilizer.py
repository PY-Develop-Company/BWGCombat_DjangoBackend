from rest_framework import serializers
from .models import Swap, Transfer


class SwapSerializer(serializers.ModelSerializer):

    class Meta:
        model = Swap
        fields = "__all__"

class TransferSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transfer
        fields = "__all__"