from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import ConnectionForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def connect(request):

    error = False

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


def disconnect(request):

    logout(request)
    return HttpResponseRedirect(reverse('account:signin'))


@login_required()      # By default, use LOGIN_URL in settings
def profil(request, user_id):
    return render(request, 'account/profil.html', locals())






