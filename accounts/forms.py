from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model

from .models import City, HealthCenter, Village


class ManagerCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            'user_type', 'username', 'first_name', 'last_name', 'gender', 'birthday', 'cell_phone', 'province', 'city',)


class ManagerChangeForm(UserChangeForm):
    GENDER_CHOICES = (
        ('man', 'Man'),
        ('women', 'Women'),
        ('other', 'Other'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Gender')

    class Meta:
        model = get_user_model()
        fields = (
            'user_type', 'username', 'first_name', 'last_name', 'gender', 'birthday', 'cell_phone', 'province', 'city',
        )


class ExpertCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = (
            'user_type', 'username', 'first_name', 'last_name', 'gender', 'birthday', 'cell_phone', 'province', 'city',
            'health_center',)


class ExpertChangeForm(UserChangeForm):
    GENDER_CHOICES = (
        ('man', 'Man'),
        ('women', 'Women'),
        ('other', 'Other'),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label='Gender')

    class Meta:
        model = get_user_model()
        fields = (
            'user_type', 'username', 'first_name', 'last_name', 'gender', 'birthday', 'cell_phone', 'province', 'city',
            'health_center',
        )


class BehvarzCreationForm(UserCreationForm):
    user_type = forms.CharField(initial='behvarz')

    class Meta:
        model = get_user_model()
        fields = ('username', 'user_type', 'gender', 'birthday', 'education', 'first_name', 'last_name', 'cell_phone',
                  'province', 'city', 'health_center', 'village',)


class BehvarzChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username', 'user_type', 'education', 'gender', 'birthday', 'first_name', 'last_name', 'cell_phone',
            'province', 'city', 'health_center', 'village',)


class CityCreateForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ('name',)


class HealthCenterForm(forms.ModelForm):
    class Meta:
        model = HealthCenter
        fields = ('name',)


class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = ('name',)
