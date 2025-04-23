from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Handles validation and creation.
    """

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        validators=[validate_password],  # Use Django's password validators
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirm password",
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ("email", "full_name", "password", "password2")
        extra_kwargs = {"full_name": {"required": True}, "email": {"required": True}}

    def validate_email(self, value):
        """
        Check if the email is already taken.
        """
        # Normalize email before checking uniqueness (optional but good practice)
        normalized_email = User.objects.normalize_email(value)
        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return normalized_email  # Return normalized email

    def validate(self, attrs):
        """
        Check that the two password entries match.
        """
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        # Password validation via validators=[validate_password] happens automatically
        # by DRF field validation if validators are specified on the field.
        # If you wanted to run them here manually (e.g., if not set on the field):
        # try:
        #     validate_password(attrs['password'])
        # except DjangoValidationError as e:
        #     raise serializers.ValidationError({'password': list(e.messages)})

        return attrs

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        Uses the custom user manager's create_user method.
        """
        # Remove the confirmation password field as it's not part of the User model
        validated_data.pop("password2")
        # Extract the password to pass separately to create_user
        password = validated_data.pop("password")

        # Use the UserManager.create_user method which handles password hashing
        user = User.objects.create_user(
            **validated_data,  # Includes email, full_name, etc.
            password=password,
        )
        # create_user already saves the user and hashes the password.
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "full_name", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]
