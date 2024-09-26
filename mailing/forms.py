from django import forms
from django.forms import BooleanField

from mailing.models import Client, EmailSetting, MailingLog


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:

        model = Client
        fields = '__all__'

class EmailSettingForm(StyleFormMixin, forms.ModelForm):
    class Meta:

        model = EmailSetting
        fields = '__all__'

class MailingLogForm(StyleFormMixin, forms.ModelForm):
    class Meta:

        model = MailingLog
        fields = '__all__'

