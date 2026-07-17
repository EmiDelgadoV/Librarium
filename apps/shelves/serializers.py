from rest_framework import serializers
from .models import Shelf

class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ['id', 'user', 'name', 'books']
        read_only_fields = ['id', 'user']