from django import forms
from .models import Instruction, Attachment
from accounts.models import CustomUser


class InsChangeForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.HiddenInput(),
        disabled=True
    )
    selected_attachments = forms.ModelMultipleChoiceField(
        queryset=Attachment.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='فایل‌های ضمیمه'
    )

    class Meta:
        model = Instruction
        fields = {'type', 'user', 'status', 'title', 'description', 'number', 'for_behvarz', 'for_expert'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['selected_attachments'].queryset = self.instance.instruction_attach.all()


class InstructionForm(forms.ModelForm):
    attachments = forms.ModelMultipleChoiceField(
        queryset=Attachment.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Instruction
        fields = {'type', 'status'}
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'q': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'جستجو'}),
        }
