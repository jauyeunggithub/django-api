# myapp/serializers.py
from rest_framework import serializers
from .models import Animal, Dog, Cat


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'


class DogSerializer(AnimalSerializer):
    class Meta:
        model = Dog
        fields = '__all__'


class CatSerializer(AnimalSerializer):
    class Meta:
        model = Cat
        fields = '__all__'
