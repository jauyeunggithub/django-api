from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    animal_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Dog(Animal):
    breed = models.CharField(max_length=100)


class Cat(Animal):
    color = models.CharField(max_length=100)
