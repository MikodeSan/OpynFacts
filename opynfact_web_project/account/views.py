from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import ConnectionForm, SignUpForm, SignUpPasswordForm, ParagraphErrorList

from enum import Enum, auto

# from ..product.models import ZSearch

class ZSign(Enum):
    UP = auto()
    CONFIRM = auto()
    PASSWORD = auto()
    UP_VALID = auto()
    IN = auto()
    IN_VALID = auto()
    OUT = auto()


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def connect(request):

    error = False
    sign_id = ZSign.IN
    sign_enum = ZSign.__members__

    # user = User.objects.create_user('Maxime', 'maxime@gmail.com', 'mypassword')
    # user.last_name = 'Lennon'
    # user.save()
    # return render(request, 'account/confirm.html')

    template = 'account/index.html'

    if request.method == "POST":
        form = ConnectionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                template = 'account/profil.html'
                return HttpResponseRedirect(reverse('account:profile', kwargs={'user_id': user.id}))
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnectionForm()

    return render(request, template, locals())

def signup(request):
    
    sign_id = ZSign.UP
    sign_enum = ZSign.__members__
    template = 'account/index.html'

    if request.method == "POST":
        form = SignUpForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            new_email = form.cleaned_data['user_mail']

            try:
                user = User.objects.get(username=new_email)
                print(user)
            except ObjectDoesNotExist:
                print('ObjectDoesNotExist')
                sign_id = ZSign.PASSWORD
                pwd_form = SignUpPasswordForm(initial={'user_mail': new_email})
                # form.fields['user_mail'].initial = new_email
            else:
                errors = {'err': 'email déjà existant'}.items()

            # password = form.cleaned_data['user_password']
        else:
            errors = form.errors.items()
    else:
        form = SignUpForm()

    print(locals())
    return render(request, template, locals())


def signup_password(request):

    sign_id = ZSign.PASSWORD
    sign_enum = ZSign.__members__
    template = 'account/index.html'

    if request.method == "POST":
        pwd_form = SignUpPasswordForm(request.POST, error_class=ParagraphErrorList)
        if pwd_form.is_valid():
            email = pwd_form.cleaned_data['user_mail']
            password = pwd_form.cleaned_data['user_password']
            password_confirmed = pwd_form.cleaned_data['user_password_confirm']

            if password == password_confirmed:
                user = User.objects.create_user(email, email, password)
                if user:
                    login(request, user)
                    return HttpResponseRedirect(reverse('product:home'))
                else:
                    errors = {'err': "Critical error: User not logged in"}.items()
            else:
                errors = {'err': "Mots de passe différents"}.items()
        else:
            errors = pwd_form.errors.items()
    else:
        errors = {'err': "Erreur d'initialisation"}.items()
        print("Sign-up password: Initialisation Error")
        return HttpResponseRedirect(reverse('account:signup'))

    return render(request, template, locals())


def disconnect(request):

    logout(request)
    return HttpResponseRedirect(reverse('product:home'))


@login_required()      # By default, use LOGIN_URL in settings
def profil(request, user_id):
    return render(request, 'account/profil.html', locals())






