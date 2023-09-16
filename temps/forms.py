from django import forms

from .models import Device
# from accounts.models import CustomUser, Province, City, HealthCenter, Village


class UploadFileForm(forms.Form):
    txt_file = forms.FileField()

