from django import forms
from django.core import validators
from django.contrib.auth.models import User

class JoinForm(forms.ModelForm):
    username = forms.CharField(help_text=False)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

def validate_location(value):
    if (value[0] != "r") or (not value[1].isdigit()) or (value[2] != "c") or (not value[3].isdigit()):
        print("raising error")
        raise forms.ValidationError("Use row and column format, e.g. r1c2.")

class ChessForm(forms.Form):
    Move_From=forms.CharField(min_length=4, max_length=4, strip=True,
    widget=forms.TextInput(attrs={'placeholder':'r2c2','style':'font-size:small'}),
    validators=[validators.MinLengthValidator(4),
    validators.MaxLengthValidator(4),
    validate_location]
    )

    Move_To=forms.CharField(min_length=4, max_length=4, strip=True,
    widget=forms.TextInput(attrs={'placeholder':'r4c2','style':'font-size:small'}),
    validators=[validators.MinLengthValidator(4),
    validators.MaxLengthValidator(4),
    validate_location]
    )
