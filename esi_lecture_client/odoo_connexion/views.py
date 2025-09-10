from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings


from .forms import UserForm
from .models import User

import xml_rpc as xml_rpc


class IndexView(TemplateView):
    template_name = "odoo_connexion/index.html"

class FormView(ListView):
    model = User
    template_name = "odoo_connexion/loginForm.html"
    context_object_name = "odoo_connexion"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userForm'] = UserForm
        return context   

def _write_info(login, username):
    with open(settings.BASE_DIR / '.env', 'w') as f:
        f.write(f"{login},{username}")


def connect(request):
    form = UserForm(request.POST)
     # Un Model Form ne sera pas valide si un champ est déjà dans la DB (très ennuyeux)
    # Nous devons essayer avec la clause else pour voir si la connexion à Odoo fonctionne
    # Beaucoup de code à copier ici
    if form.is_valid():
        login, password = form.cleaned_data['login'], form.cleaned_data['password']
        try:
            uid = xml_rpc.connect(login, password)
            if uid:
                User.objects.create(
                    login=login,
                    password=password,
                )
                _write_info(login, password)
                messages.success(request, "Identification réussie !")
            else:
                messages.error(request, "L'identification a échoué.")
        except ConnectionError:
            messages.error(request, "Le serveur Odoo n'est pas démarré !")
    else:
        login, password = form.data['login'], form.data['password']  # data and not cleaned_data
        try:
            uid = xml_rpc.connect(login, password)
            if uid:
                user = User.objects.get(
                    login=login,
                    password=password,
                )
                if user:
                    messages.success(request, "Identification réussie !")
                    _write_info(login, password)
            else:
                messages.error(request, "L'identification a échoué.")
        except ConnectionError:
            messages.error(request, "Le serveur Odoo n'est pas démarré !")
    # redirection vers le site après la requête POST
    # redirection après la gestion correcte pour empêcher de poster deux fois
    return HttpResponseRedirect(reverse('odoo_connexion:loginForm'))        

   
