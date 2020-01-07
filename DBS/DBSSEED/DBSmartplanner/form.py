from django import forms
from .models import UserLoginModel

class LoginForm(forms.ModelForm):
    class Meta:
        model = UserLoginModel
        fields = ['username','password']
        labels = {'username':'username', 'password':'password'}

        widgets = {
            'password': forms.PasswordInput(),
        }

        def __str__(self):
            return self.usernmae