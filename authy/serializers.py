from __future__ import annotations

from django.conf import settings
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import ModelSerializer, Serializer

from authy.models import User, UserOTP, PendingUser, VerificationCode
from services.code_generators import CodeGenerator
from authy.tasks import *
from services.utlis import refresh_token
from authy.services import generate_otp


class PendingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingUser
        fields = (
            "full_name",
            "phone_number",
            "password",
            "email",
            # "user_type",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        return make_password(value)

    @transaction.atomic
    def create(self, validated_data):
        otp_code = CodeGenerator.generate_otp(4)
        user = User.objects.filter(email=validated_data.get("email")).first()
        if user:
            raise serializers.ValidationError(
                {"error": "User with this email already exist"}
            )

        user = User.objects.filter(
            phone_number=validated_data.get("phone_number")
        ).first()
        if user:
            raise serializers.ValidationError(
                {"error": "User with this phone number already exist"}
            )
        try:
            pending_user = PendingUser.objects.get(email=validated_data.get("email"))
        except PendingUser.DoesNotExist:
            pending_user = PendingUser.objects.create(**validated_data)

        pending_code = generate_otp(pending_user=pending_user, otp_code=otp_code)
        send_account_activation_email(validated_data.get("email"), pending_code.code)

        return pending_user


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "full_name",
            "phone_number",
            "password",
            "email",
            "id",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        token = refresh_token(instance)
        rep["token"] = token
        if instance.is_verified:
            rep["picture"] = (
                settings.CLOUDINARY_ROOT_URL + str(instance.picture)
                if instance.picture
                else None
            )

        return rep

    def validate_password(self, value):
        return make_password(value)

    def validate(self: UserSerializer, data: dict):
        return data

    @transaction.atomic
    def create(self, validated_data):
        otp_code = CodeGenerator.generate_otp(4)
        validated_data["otp"] = otp_code

        user = User.objects.create(**validated_data)
        try:
            otp, is_new = UserOTP.objects.get_or_create(
                user=user, defaults={"user": user, "secret": otp_code}
            )

            if not is_new:
                otp.delete()
                otp = UserOTP.objects.create(user=user, secret=otp_code)
        except Exception as a:
            print(f"\n\n Error:{a}\n\n")
        send_account_activation_email(validated_data.get("email"), otp_code)

        return user


class UpdateUserSerializer(ModelSerializer):
    token = serializers.StringRelatedField(source="auth_token.key", read_only=True)

    class Meta:
        model = User
        fields = (
            "full_name",
            "phone_number",
            "password",
            "email",
            "id",
            "token",
            "picture",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.is_verified:
            token = refresh_token(instance)
            rep["token"] = token
            rep["picture"] = (
                settings.CLOUDINARY_ROOT_URL + str(instance.picture)
                if instance.picture
                else None
            )
            rep["state_name"] = instance.state.name if instance.state else None

        return rep

    def update(self, instance: User, validated_data):
        instance.is_available = validated_data.get(
            "is_available", instance.is_available
        )
        instance.picture = validated_data.get("picture", instance.picture)
        instance.state = validated_data.get("state", instance.state)
        instance.address = validated_data.get("address", instance.address)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50, write_only=True)
    password = serializers.CharField(max_length=50, write_only=True)
    token = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "token", "id", "user_type"]
        read_only_fields = ("token",)

    def validate(self, data):
        password = data.get("password", "")
        email = data.get("email", "")
        try:
            user = User.objects.get(email__iexact=email)
            valid_credentials = user.check_password(password)
        except User.DoesNotExist:
            user = None
            valid_credentials = None
        # print(f"\n\nThe valid credentials {valid_credentials} {email} {password}\n\n")
        if not valid_credentials:
            raise AuthenticationFailed("Invalid credentials, try again")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")

        if not user.is_verified:
            raise AuthenticationFailed("Please verify your email and try again")

        refresh_token(user)
        user.first_login = False
        user.save()
        data = UserSerializer(user).data
        data["user_type"] = user.user_type
        return data

    def create(self, validated_data):
        return validated_data


class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()


class RequestNewOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2, max_length=100)


class UpdatePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=50, write_only=True)
    secret = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        fields = ["old_password", "new_password", "secret"]


class UpdatePasswordInAppSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50, write_only=True)
    new_password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        fields = ["old_password", "new_password"]


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)

    class Meta:
        fields = ["password"]

    def validate(self, data):
        password = data.get("password")
        otp = self.context.get("token")
        try:
            user_otp = UserOTP.objects.get(secret=otp)
            user = user_otp.user
        except UserOTP.DoesNotExist:
            raise AuthenticationFailed("The reset otp is invalid try again", 401)

        user.set_password(password)
        user_otp.delete()
        user.save()
        token = refresh_token(user)
        send_update_password_succcess_email(user.email)
        return {"email": user.email, "token": token}


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    @transaction.atomic
    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        try:
            pending_user = PendingUser.objects.get(email=email)
            user_otp = VerificationCode.objects.get(pending_user=pending_user)
        except (PendingUser.DoesNotExist, VerificationCode.DoesNotExist):
            raise serializers.ValidationError("Invalid email or OTP.")

        if user_otp.code != otp:
            raise serializers.ValidationError("The OTP is incorrect.")

        return data

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data.get("email")

        # Retrieve pending user
        pending_user = PendingUser.objects.get(email=email)

        # Create the actual user
        user = User.objects.create(
            full_name=pending_user.full_name,
            phone_number=pending_user.phone_number,
            password=pending_user.password,
            email=pending_user.email,
        )

        # Clean up: delete pending user and OTP
        UserOTP.objects.filter(pending_user=pending_user).delete()
        VerificationCode.objects.filter(pending_user=pending_user).delete()
        pending_user.delete()

        return user
