from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Job, CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'company_name',)


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description']


class EmployerUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['company_name', 'phone_number']


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['skills', 'desired_salary', 'experience', 'phone_number']
