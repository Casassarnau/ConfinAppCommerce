from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password

from hackovid import settings
from user.models import User


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Contrasenya"),
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
    email = forms.EmailField(required=True, label='',
                             widget=forms.EmailInput(attrs={'placeholder': 'Correu electrònic'}))
    password = forms.CharField(required=True, label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Contrasenya'}))

    # function used to see the type of form in the template
    def is_login(self):
        return True


class RegisterForm(LoginForm):
    password2 = forms.CharField(label='', required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirma la contrasenya'}), )
    name = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Nom'}))

    field_order = ['name', 'email', 'password', 'password2']

    # if the passwords don't match raise error
    def clean_password2(self):

        # get passwords from form
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        # raise error if passwords don't match
        if password2 and password and password2 != password:
            raise forms.ValidationError('Les contrasenyes no coincideixen')

        # validates if the password is secure
        validate_password(password)
        return password2

    # function used to see the type of form in the template
    def is_login(self):
        return False


class RegisterShopAdminForm(RegisterForm):
    token = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Codi de registre'}))

    # validate if the token is the correct one
    def clean_token(self):

        # get token from settings and from settings
        validToken = getattr(settings, 'REGISTRATION_CODE', '')
        token = self.cleaned_data['token']

        # raise error if token is invalid
        if token and token != validToken:
            raise forms.ValidationError('Codi de registre invàlid')
        return token
