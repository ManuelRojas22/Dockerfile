"""Formularios de la app core."""

from django import forms

from apps.core.models import ContactMessage


class StyledFormMixin:
    """Aplica las clases CSS de los estilos del frontend."""

    css_class = "campo"

    def _style_fields(self) -> None:
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {self.css_class}".strip()
            field.widget.attrs.setdefault("autocomplete", "off")


class ContactForm(StyledFormMixin, forms.ModelForm):
    """Formulario de contacto del pie de pagina."""

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        labels = {
            "name": "Nombre",
            "email": "Correo electronico",
            "subject": "Asunto",
            "message": "Mensaje",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Tu nombre"}),
            "email": forms.EmailInput(attrs={"placeholder": "tu@correo.com"}),
            "subject": forms.TextInput(attrs={"placeholder": "Sobre que nos escribes"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Escribe tu mensaje"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def clean_message(self) -> str:
        message = (self.cleaned_data.get("message") or "").strip()
        if len(message) < 10:
            raise forms.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return message
