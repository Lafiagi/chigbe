from authy.models import VerificationCode


def generate_otp(pending_user, otp_code):
    pending_code, created = VerificationCode.objects.get_or_create(
        pending_user=pending_user,
        defaults={"pending_user": pending_user, "code": otp_code},
    )
    if not created:
        pending_code.delete()
        pending_code, _ = VerificationCode.objects.get_or_create(
            pending_user=pending_user,
            defaults={"pending_user": pending_user, "code": otp_code},
        )
    return pending_code
