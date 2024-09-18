from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        # Проверка на уникальность email
        if self.model.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")

        # Проверка на уникальность username
        if self.model.objects.filter(username=username).exists():
            raise ValidationError("A user with this username already exists.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Token.objects.create(user=user)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Почта"), unique=True)
    password = models.CharField(_("Пароль"), max_length=128)
    username = models.CharField(_("Логин"), max_length=150)
    first_name = models.CharField(_("Имя"), max_length=30)
    last_name = models.CharField(_("Фамилия"), max_length=30)
    patronymic = models.CharField(_("Отчество"), max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "patronymic"]

    def __str__(self):
        return self.email


class Defect(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "defect"
        verbose_name_plural = "defects"

    def __str__(self):
        return self.name


class DefectStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "defect_status"
        verbose_name_plural = "defect statuses"

    def __str__(self):
        return self.name


class Mark(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images/")

    class Meta:
        db_table = "mark"
        verbose_name_plural = "marks"


class MarkAnnotation(models.Model):
    mark_id = models.ForeignKey(Mark, on_delete=models.CASCADE, db_column="mark_id")
    defect_id = models.ForeignKey(Defect, on_delete=models.CASCADE, db_column="defect_id")
    defect_status = models.ForeignKey(DefectStatus, on_delete=models.CASCADE, db_column="defect_status")

    class Meta:
        db_table = "mark_annotation"
        verbose_name_plural = "mark annotations"
