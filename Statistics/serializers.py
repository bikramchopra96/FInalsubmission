from rest_framework import serializers

from .models import YearlyTable

class api_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YearlyTable
        fields = ('productdate','index', 'timestamp','high', 'low', 'open', 'close','volume')