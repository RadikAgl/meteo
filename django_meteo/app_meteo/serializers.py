from rest_framework import serializers


class CityHistorySerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    count = serializers.IntegerField()

    class Meta:
        ordering = ['-count']
