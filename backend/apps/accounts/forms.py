"""Formularios de registro, login y perfil."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from apps.core.forms import StyledFormMixin
from apps.accounts.models import Profile
from apps.accounts.services import AuthService


class RegisterForm(StyledFormMixin, UserCreationForm):
    """Registro de usuarios nuevos."""

    first_name = forms.CharField(label="Nombre", max_length=60, required=True)
    last_name = forms.CharField(label="Apellido", max_length=60, required=True)
    email = forms.EmailField(label="Correo electronico", required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {"username": "Usuario"}
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "usuario123"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Nombre"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Apellido"}),
            "email": forms.EmailInput(attrs={"placeholder": "tu@correo.com"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = "Solo letras, numeros y . _ -"
        self.fields["password1"].label = "Contrasena"
        self.fields["password2"].label = "Repetir contrasena"
        self._style_fields()

    def clean_email(self) -> str:
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo.")
        return email

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            Profile.objects.create(user=user)
        return user


class LoginForm(StyledFormMixin, AuthenticationForm):
    """Inicio de sesion (acepta usuario o correo electronico)."""

    username = forms.CharField(
        label="Usuario o correo", widget=forms.TextInput(attrs={"placeholder": "usuario123"})
    )
    password = forms.CharField(
        label="Contrasena", widget=forms.PasswordInput(attrs={"placeholder": "••••••••"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def clean(self):
        """Autentica con AuthService (resuelve correo -> usuario)."""
        cleaned_data = super(AuthenticationForm, self).clean()

        username = (cleaned_data.get("username") or "").strip()
        password = cleaned_data.get("password") or ""

        self.user_cache = None
        if username and password:
            self.user_cache = AuthService.authenticate(self.request, username, password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Usuario o contrasena incorrectos.", code="invalid_login"
                )
            self.confirm_login_allowed(self.user_cache)

        return cleaned_data


class ProfileForm(StyledFormMixin, forms.ModelForm):
    """Edicion del perfil propio."""

    class Meta:
        model = Profile
        fields = ("company", "role", "bio", "avatar_url")
        labels = {
            "company": "Empresa",
            "role": "Cargo",
            "bio": "Biografia",
            "avatar_url": "URL del avatar",
        }
        widgets = {
            "company": forms.TextInput(attrs={"placeholder": "Acme S.A.S."}),
            "role": forms.TextInput(attrs={"placeholder": "DevOps Engineer"}),
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Cuenta de como trabajas"}),
            "avatar_url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
