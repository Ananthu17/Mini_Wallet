from rest_framework import serializers
from .models import *

class Userserializers(serializers.ModelSerializer):
    class Meta :
        model= Customer
        fields = ['token']