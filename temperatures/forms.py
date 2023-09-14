from django import forms
from .models import DeviceInformation
from accounts.models import CustomUser, Province, City, HealthCenter, Village


class UploadFileForm(forms.ModelForm):
    txt_file = forms.FileField()

    class Meta:
        model = DeviceInformation
        fields = ['user', 'province', 'city', 'health_center', 'village']
