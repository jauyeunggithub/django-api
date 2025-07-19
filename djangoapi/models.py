# myapp/models.py
from django.db import models
from polymorphic.models import PolymorphicModel

# Base class for polymorphic models


class Animal(PolymorphicModel):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name

# A dog inherits from Animal


class Dog(Animal):
    breed = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.breed}"

# A cat inherits from Animal


class Cat(Animal):
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.color}"
