from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        # Ensure the user is not staff or superuser
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        return user