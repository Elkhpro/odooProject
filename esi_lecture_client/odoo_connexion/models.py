from django.db import models


# Create your models here.

class User(models.Model):
    login = models.CharField("login", max_length=200)
    password = models.CharField("password", max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint('login', name='unique_login')
        ]