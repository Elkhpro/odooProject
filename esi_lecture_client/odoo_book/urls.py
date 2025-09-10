from django.urls import path
from . import views
from .views import BookView

app_name = 'odoo_book'
urlpatterns = [
    path('', BookView.index, name="index"),
    path('addLike/<int:book_id>', BookView.addLike, name="addLike"),
    ]