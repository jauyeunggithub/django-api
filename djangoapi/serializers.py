from rest_framework import serializers
from drf_polymorphic.serializers import PolymorphicSerializer
from drf_writable_nested import WritableNestedModelSerializer
from .models import Animal, Dog, Cat
from rest_framework.exceptions import ValidationError

# Dog serializer


class DogSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Dog
        # 'animal_type' should be in the fields for the specific model serializer
        fields = ['id', 'name', 'age', 'animal_type', 'breed']

# Cat serializer


class CatSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Cat
        # 'animal_type' should be in the fields for the specific model serializer
        fields = ['id', 'name', 'age', 'animal_type']

# Animal serializer (base class for polymorphism)


class AnimalSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Animal
        # 'animal_type' should be in the fields for the specific model serializer
        fields = ['id', 'name', 'age', 'animal_type']


# Polymorphic serializer that maps the 'animal_type' to the correct serializer
class AnimalPolymorphicSerializer(PolymorphicSerializer):
    discriminator_field = 'animal_type'
    animal_type = serializers.CharField(read_only=True)

    serializer_mapping = {
        'dog': DogSerializer,  # Map 'dog' to DogSerializer
        'cat': CatSerializer,  # Map 'cat' to CatSerializer
        'animal': AnimalSerializer,  # Default serializer for Animal
    }

    def is_valid(self, raise_exception=False):
        if self.initial_data.get(self.discriminator_field) is None:
            raise ValidationError(f"'{self.discriminator_field}' is required")

        return super().is_valid(raise_exception=raise_exception)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if isinstance(instance, Dog):
            representation['breed'] = instance.breed

        return representation

    def create(self, validated_data):
        animal_type = validated_data.pop(self.discriminator_field, None)
        if not animal_type:
            raise ValidationError(
                f"'{self.discriminator_field}' is required for creation.")

        if animal_type not in self.serializer_mapping:
            raise ValidationError(f"Invalid animal type: {animal_type}")

        ChildSerializer = self.serializer_mapping[animal_type]
        validated_data[self.discriminator_field] = animal_type
        child_serializer = ChildSerializer(data=self.initial_data)
        child_serializer.is_valid(raise_exception=True)

        instance = child_serializer.save()
        return instance

    def update(self, instance, validated_data):
        animal_type = validated_data.pop(self.discriminator_field, None)
        if not animal_type:
            animal_type = getattr(instance, self.discriminator_field, None)

        if not animal_type or animal_type not in self.serializer_mapping:
            raise ValidationError(
                f"Invalid or missing animal type for update: {animal_type}")

        ChildSerializer = self.serializer_mapping[animal_type]
        validated_data[self.discriminator_field] = animal_type
        child_serializer = ChildSerializer(
            instance, data=validated_data, partial=True)
        child_serializer.is_valid(raise_exception=True)
        instance = child_serializer.save()
        return instance
