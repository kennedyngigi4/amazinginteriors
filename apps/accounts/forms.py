from django import forms
from django.contrib.auth import authenticate

from apps.accounts.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # extra_kwargs = { "write_only": { "password": True } }
        fields = [
            "fullname", "email", "password"
        ]



class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise forms.ValidationError("Invalid Email or Password")
        return self.cleaned_data


