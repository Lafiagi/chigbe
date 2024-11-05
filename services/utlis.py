from authy.models import User, PendingUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
import random
import string


def refresh_token(user: User) -> str:
    token = RefreshToken.for_user(user)
    response = {
        "refresh": str(token),
        "access": str(token.access_token),
    }
    return response


def check_user_exists(email, phone_number):
    user = User.objects.filter(email=email).first()
    if user:
        raise serializers.ValidationError(
            {"error": ["User with this email already exist"]}
        )

    user = User.objects.filter(phone_number=phone_number).first()
    if user:
        raise serializers.ValidationError(
            {"error": ["User with this phone number already exist"]}
        )
    return False


def create_pending_user(validated_data):
    try:
        pending_user = PendingUser.objects.get(email=validated_data.get("email"))
    except PendingUser.DoesNotExist:
        pending_user = PendingUser.objects.create(**validated_data)

    return pending_user


def generate_unique_code(app_id):
    return f"PRD-{app_id}-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
