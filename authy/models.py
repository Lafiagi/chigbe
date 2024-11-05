from __future__ import annotations

from typing import Dict, List
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from cloudinary.models import CloudinaryField
from services.code_generators import CodeGenerator
from generics.base_model import BaseModel
from authy.managers import UserManager


class BaseSoftDeletableModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(
        auto_now=True,
    )
    deleted_by = models.ForeignKey("User", null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def soft_delete(self, user_id=None):
        self.is_deleted = True
        self.deleted_by = user_id
        self.save()


class User(AbstractUser, BaseModel, BaseSoftDeletableModel):
    email = models.EmailField(unique=True, verbose_name="E-mail Address")
    full_name = models.CharField(max_length=150, blank=True, verbose_name="First Name")
    phone_number = models.CharField(
        unique=True, max_length=20, blank=True, null=True, verbose_name="Phone Number"
    )
    picture = CloudinaryField("profile_pic", null=True, blank=True)
    first_login = models.BooleanField(default=True, verbose_name="First Login")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")
    user_type = models.TextField(choices=(("client", "client"), ("enterprise", "enterprise")), default="client")
    objects = UserManager()
    REQUIRED_FIELDS = ["full_name", "phone_number"]
    USERNAME_FIELD: str = "email"

    class Meta:
        ordering = ("email",)

    def __str__(self: AbstractUser):
        return f"{self.email}"

    def save(self: User, *args: List[str], **kwargs: Dict) -> None:
        if not self.username:
            digit = CodeGenerator.generate_otp(2)
            email = self.email
            self.username = str(email).split("@")[0]
            self.username += str(digit)

        super().save(*args, **kwargs)


class PendingUser(BaseModel):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    email = models.EmailField()

    def __str__(self):
        return self.full_name


class Business(BaseModel):
    user = models.OneToOneField("authy.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} owned by {self.user.username}"


class VerificationCode(BaseModel):
    user = models.OneToOneField("User", null=True, blank=True, on_delete=models.CASCADE)
    pending_user = models.OneToOneField(
        "PendingUser", null=True, blank=True, on_delete=models.CASCADE
    )
    code = models.CharField(max_length=150, default=uuid4, editable=False, unique=True)

    def __str__(self) -> str:
        name = self.user.full_name if self.user else self.pending_user.full_name
        return f"{name} code: {self.code}"


class UserOTP(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret = models.CharField(max_length=50, default=uuid4)
    pending_user = models.OneToOneField(
        "PendingUser", null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        name = self.user.full_name if self.user else self.pending_user.full_name
        return f"{name} code: {self.secret}"
