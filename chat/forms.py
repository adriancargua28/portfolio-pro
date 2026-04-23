from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Conversation, AVAILABLE_MODELS


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email (opcional)")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ["title", "model"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título de la conversación"}),
            "model": forms.Select(attrs={"class": "form-select"}, choices=AVAILABLE_MODELS),
        }


class MessageForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Escribe tu mensaje...",
            "id": "message-input",
        }),
        label="",
    )
    context_text = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 2,
            "placeholder": "Fragmento de contexto adicional (opcional, máx. 2000 caracteres)",
        }),
        required=False,
        label="Contexto adicional",
        max_length=2000,
    )


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Buscar conversaciones..."}),
        label="",
    )
