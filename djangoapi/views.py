from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from rest_framework import viewsets
from .models import Animal
from .serializers import AnimalPolymorphicSerializer
from rest_framework.exceptions import NotFound, ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [TokenAuthentication]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Send a welcome email after successful registration
            send_mail(
                'Welcome to Our Site',
                'Thank you for registering with us.',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"detail": "User created successfully!"})
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def send_email(self, request):
        """Custom action to send an email to a specified user"""
        email = request.data.get('email')
        subject = request.data.get('subject', 'No Subject')
        message = request.data.get('message', 'No Message')

        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            # Send the email
            send_mail(
                subject,
                message,
                'from@example.com',  # Use a proper sender email
                [email],
                fail_silently=False,
            )
            return Response({"detail": "Email sent successfully!"})
        except Exception as e:
            return Response({"error": f"Failed to send email: {str(e)}"}, status=500)


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalPolymorphicSerializer
    lookup_field = 'id'

    def get_object(self):
        """
        Override this method if you want to handle optional lookup for 'id'.
        """
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_field

        if not self.kwargs.get(lookup_url_kwarg):
            return queryset.first()  # Return the first object if no 'id' is provided

        return super().get_object()

    def perform_create(self, serializer):
        """
        Override to handle creating an animal. Ensure 'animal_type' is included.
        """
        animal_type = self.request.data.get('animal_type')
        if not animal_type:
            raise ValidationError({"animal_type": "This field is required."})

        if animal_type not in ['dog', 'cat', 'animal']:
            raise ValidationError(
                {"animal_type": f"Invalid animal type: {animal_type}"})

        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Override the create method to handle creation with validation.
        """
        animal_type = request.data.get('animal_type')
        if not animal_type:
            raise ValidationError({"animal_type": "This field is required."})

        if animal_type not in ['dog', 'cat', 'animal']:  # Add valid animal types here
            raise ValidationError(
                {"animal_type": f"Invalid animal type: {animal_type}"})

        return super().create(request, *args, **kwargs)
