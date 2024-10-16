from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm

from mailing.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        """Скрывает информацию про пароль в форме"""
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    """Форма на сброс пароля"""

    class Meta:
        model = User
        fields = ('email',)
