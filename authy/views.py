import cloudinary
from django.db.transaction import atomic
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from authy.models import *
from authy.tasks import *
from authy.serializers import *
from services.utlis import refresh_token


class UserRegistrationViewset(ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ["post"]
    permission_classes = (AllowAny,)


class OnboardingUserRegistrationViewset(ModelViewSet):
    serializer_class = PendingUserSerializer
    http_method_names = ["post"]
    permission_classes = (AllowAny,)


class UpdateUserView(ModelViewSet):
    serializer_class = UpdateUserSerializer
    http_method_names = ["post", "patch"]
    queryset = User.objects.all()


class SigninView(GenericAPIView):
    serializer_class = UserLoginSerializer
    http_method_names = ["post"]
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RequestNewOTPView(GenericAPIView):
    permission_classes = []
    serializer_class = RequestNewOTPSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.validated_data
        user = User.objects.get(email=user_data["email"])
        if user.is_verified:
            return Response(
                {"data": "email is already verified"},
                status=status.HTTP_200_OK,
            )
        otp = CodeGenerator.generate_otp(4)
        send_account_activation_email(user_data.get("email"), otp)
        user.otp = otp
        user.save()

        return Response(
            {"data": "OTP sent to " + str(user_data["email"]) + " successfully"},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(GenericAPIView):
    serializer_class = OTPSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    @transaction.atomic
    def post(self, request):
        otp = request.data.get("otp")
        email = request.data.get("email")
        try:
            user_otp = VerificationCode.objects.get(code=otp, pending_user__email=email)
            pending_user = user_otp.pending_user
            user = User.objects.create(
                full_name=pending_user.full_name,
                phone_number=pending_user.phone_number,
                password=pending_user.password,
                email=pending_user.email,
                user_type=pending_user.user_type,
            )
            pending_user.delete()
            user_otp.delete()
        except (PendingUser.DoesNotExist, VerificationCode.DoesNotExist, Exception):
            raise serializers.ValidationError({"error": "Invalid email or OTP."})

        if user.is_verified:
            raise serializers.ValidationError({"error": "Account is already Verified!"})

        user.is_verified = True
        user.save()
        send_account_verified_email(user.email)
        message = "Successfully verified email, proceed to login"
        return Response(
            {"message": message, "data": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )


class UpdatePasswordView(GenericAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = (AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = request.data.get("new_password", "")
        secret = request.data.get("secret", "")

        try:
            user = UserOTP.objects.get(secret=secret).user
        except UserOTP.DoesNotExist:
            return Response(
                {"errors": "Wrong Password Token "},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            user.set_password(new_password)
            user.save()
            send_update_password_succcess_email(user.email)
            return Response(
                {"message": "Successfully updated your password"},
                status=status.HTTP_200_OK,
            )


class ValidateOTPView(GenericAPIView):
    serializer_class = OTPSerializer
    permission_classes = (AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        secret = request.data.get("otp", "")

        try:
            UserOTP.objects.get(secret=secret)

        except UserOTP.DoesNotExist:
            return Response(
                {"errors": "Wrong Password Token "},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Successfully verified your otp"},
            status=status.HTTP_200_OK,
        )


class UpdatePasswordInAppView(GenericAPIView):
    serializer_class = UpdatePasswordInAppSerializer
    permission_classes = (IsAdminUser,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")

        user = authenticate(email=request.user.email, password=old_password)
        if user:
            user.set_password(new_password)
            user.save()
            send_update_password_succcess_email(user.email)
            return Response(
                {"message": "Successfully updated your password"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"errors": "Wrong password"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email", "")
        code = CodeGenerator.generate_otp(4)
        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"message": "We have sent an email if it exists"},
                status=status.HTTP_200_OK,
            )

        otp, is_new = VerificationCode.objects.get_or_create(
                user=user, defaults={"user": user, "code": code}
            )

        if not is_new:
            otp.delete()
            otp = VerificationCode.objects.create(user=user, code=code)
        send_forgot_password_email(email, str(otp.code))
        return Response(
            {"message": "We have sent a password reset mail to your box if it exists"},
            status=status.HTTP_200_OK,
        )


class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def patch(self, request, token):
        serializer = self.serializer_class(data=request.data, context={"token": token})
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()

        return Response("User logged out successfully")


class VerificationCodeView(GenericAPIView):
    serializer_class = OTPVerificationSerializer
    http_method_names = ["post"]
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            VerificationCode.objects.get(code=request.data.get("code"))

        except VerificationCode.DoesNotExist:
            return Response(
                {
                    "message": "Code Not Valid, register through the chigbe mobile app to get your invitation code."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
