from django.urls import path
from rest_framework.routers import SimpleRouter

from authy.views import *


router = SimpleRouter()
router.register(r"signup", UserRegistrationViewset, basename="signup")
router.register(
    r"onboarding-signup", OnboardingUserRegistrationViewset, basename="onboarding_signup"
)
router.register(r"update-user", UpdateUserView, basename="update-user")

urlpatterns = [
    path("api/v1/signin", SigninView.as_view()),
    path("api/v1/verification-code", VerificationCodeView.as_view()),
    path("api/v1/signout", LogoutView.as_view()),
    path("api/v1/verify-email", VerifyOTPView.as_view()),
    path("api/v1/verify-otp", ValidateOTPView.as_view()),
    path("api/v1/request-new-otp", RequestNewOTPView.as_view()),
    path("api/v1/update-password", UpdatePasswordView.as_view()),
    path("api/v1/update-password-in-app", UpdatePasswordInAppView.as_view()),
    path("api/v1/forgot-password", ForgotPasswordView.as_view()),
    path("api/v1/set-password/<uuid:token>", SetNewPasswordView.as_view()),
]
urlpatterns += router.urls
