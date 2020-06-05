from django.db import models

# Create your models here.


class User(models.Model):
    password = models.CharField(max_length=6)
    last_login = models.DateField(auto_now=True)
    email = models.CharField(max_length=255)
    is_active = models.DateField(auto_now=True)
    date_joined = models.DateField(auto_now=True)

    def __str__(self):
        return self.email
