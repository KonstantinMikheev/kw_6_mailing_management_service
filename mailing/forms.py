from django import forms
from django.forms import BooleanField, DateTimeInput

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
        exclude = ('owner',)


class EmailSettingForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Предоставляет доступ к объекту запроса,
        так что в качестве параметров указаны только клиенты текущего пользователя
        """
        self.request = kwargs.pop('request')
        super(EmailSettingForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(owner=self.request.user)


    class Meta:
        model = EmailSetting
        fields = ('subject', 'body', 'description', 'periodicity', 'start_from', 'stop_at', 'is_active', 'client',)
        widgets = {
            'start_from': DateTimeInput(format='%Y-%m-%dT%H:%M',
                                        attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'stop_at': DateTimeInput(format='%Y-%m-%dT%H:%M',
                                     attrs={'type': 'datetime-local', 'class': 'form-control'})
        }

        def clean_clients(self):
            cleaned_data = self.cleaned_data['client']
            if cleaned_data.is_staff:
                raise forms.ValidationError('Автором не может быть сотрудник сайта.')


class EmailSettingManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = EmailSetting
        fields = ('is_active',)


class MailingLogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingLog
        fields = '__all__'
