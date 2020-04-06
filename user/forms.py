from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from user.models import User


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Passwords are not stored in plaintext, so there is no way to see "
                                                    "this user's password"))

    class Meta:
        model = User
        exclude = []

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label='Email')
    password = forms.CharField(required=True, label='Password', widget=forms.PasswordInput)


class RegisterForm(LoginForm):
    password2 = forms.CharField(label='Confirm password', required=True, widget=forms.PasswordInput)
    name = forms.CharField(label='Name', required=True)

    field_order = ['name', 'email', 'password', 'password2']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 and password and password2 != password:
            return forms.ValidationError('Passwords don\'t match', code='error')
        return password2



