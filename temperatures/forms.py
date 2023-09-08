from django import forms

class UploadFileForm(forms.Form):
    txt_file = forms.FileField()