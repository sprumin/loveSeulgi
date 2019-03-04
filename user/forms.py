from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from user.models import User, UserManager


class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'E-mail address',
                'required': 'true',
            }))
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'required': 'true'
            }))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'required': 'true'
            }))
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password confirmation',
                'required': 'true'
            }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserSignInForm(forms.ModelForm):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'E-mail address',
                'required': 'true',
            }))
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'required': 'true'
            }))

    class Meta:
        model = User
        fields = ('email', 'password', )


class UserDeleteForm(forms.ModelForm):
    email = forms.EmailField(
        label='E-mail',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'E-mail address',
                'required': 'true',
            }))

    class Meta:
        model = User
        fields = ('email', )
