from django.urls import path
from . import views
from .views import IndexView, FormView

app_name = 'odoo_connexion'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('loginForm', FormView.as_view(), name='loginForm'),
    path('login', views.connect, name="login")
    ]