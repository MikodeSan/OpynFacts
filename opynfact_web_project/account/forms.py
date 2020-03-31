from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from django.forms.utils import ErrorList

from .models import ZProfil


class ConnectionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class SignUpForm(forms.Form):
    user_mail = forms.EmailField(
        label="E-mail",
        # initial="Votre adresse",
        help_text="Votre adresse e-mail comme nom d'utilisateur",
        # widget=fomrs.EmailInput(attrs={'class': 'form-control'}),
        max_length=30
        )

class SignUpPasswordForm(forms.Form):
    user_mail = forms.EmailField(
        label="E-mail",
        # initial="Votre adresse",
        help_text="Votre adresse e-mail comme nom d'utilisateur",
        widget=forms.HiddenInput(),
        max_length=30
        )
    user_password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput()        # attrs={'id': 'toto'}
        )
    user_password_confirm = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput()
        )

# class SignUpForm2(ModelForm):
#     class Meta:

#         model = ZProfil
#         fields = ["user.email, user.password"]
#         widgets = {
#             'name': TextInput(attrs={'class': ''}),
#             'mail': EmailInput(attrs={'class': ''})
#         }

#         user_mail = forms.EmailField(
#             label="E-mail",
#             # initial="Votre adresse",
#             help_text="Votre adresse e-mail comme nom d'utilisateur",
#             # widget=fomrs.EmailInput(attrs={'class': 'form-control'}),
#             max_length=30
#             )
#         user_password = forms.CharField(
#             label="Mot de passe",
#             widget=forms.PasswordInput()        # attrs={'id': 'toto'}
#             )


class ParagraphErrorList(ErrorList):

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        zstr = ''
        if self: 
            s = ''.join(['<p class="small error">{}</p>'.format(err) for err in self])
            zstr = '<div class="errorlist">{}</div>'.format(s)
        return zstr