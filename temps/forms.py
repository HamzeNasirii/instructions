from django import forms
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime


class UploadFileForm(forms.Form):
    txt_file = forms.FileField()


class DateRangeForm(forms.Form):
    start_date = JalaliDateField(widget=AdminJalaliDateWidget)
    end_date = JalaliDateField(widget=AdminJalaliDateWidget)
