from rest_framework import serializers
from .models import WorldBankData


class WorldBankDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldBankData
        fields = ['id', 'country', 'series', 'year', 'value']
