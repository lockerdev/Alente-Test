from django import forms

from django.core.exceptions import ValidationError


class UploadEventFile(forms.Form):
    response_file = forms.FileField(help_text="Выберите файл для ответа")

    def clean_renewal_date(self):
        data = self.cleaned_data['response_file']
        return data
