from dataclasses import fields
from rest_framework import serializers 
from .models import *

class SongSerializer(serializers.Serializer):
    class Meta:
        model = Song
        fields = '__all__'

class SampleSerializer(serializers.Serializer):
    class Meta:
        model = Sample
        fields = '__all__'

class SongSampleSerializer(serializers.Serializer):
    class Meta:
        model = Song_Sample
        fields = '__all__'