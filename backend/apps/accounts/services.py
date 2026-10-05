"""Servicios de la app accounts."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from apps.accounts.models import Profile


class AccountService:
    """Reglas de negocio de cuentas de usuario."""

    UserModel = get_user_model()

    @classmethod
    def get_or_create_profile(cls, user: User) -> Profile:
        profile, _ = Profile.objects.get_or_create(user=user)
        return profile

    @classmethod
    def email_exists(cls, email: str) -> bool:
        return cls.UserModel.objects.filter(email__iexact=email.strip()).exists()

    @classmethod
    def count_users(cls) -> int:
        return cls.UserModel.objects.count()


class AuthService:
    """Azucar sobre la autenticacion nativa de Django."""

    @classmethod
    def authenticate(cls, request, username: str, password: str):
        from django.contrib.auth import authenticate

        user = authenticate(request, username=username, password=password)
        if user is None and "@" in username:
            user_model = get_user_model()
            match = user_model.objects.filter(email__iexact=username).first()
            if match is not None:
                user = authenticate(request, username=match.get_username(), password=password)
        return user
