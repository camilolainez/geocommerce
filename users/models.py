from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class CustomUser(AbstractUser):

    # Aquí puedo agregar los campos adicionales que necesites para el modelo users
    username = models.CharField(_('username'), max_length=150, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    schema = models.OneToOneField('accounts.Client', on_delete = models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    subscription = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    birthday = models.DateField(verbose_name=_("Birthday"), blank=True, null=True,
        validators=[
            MinValueValidator(limit_value=date(1900, 1, 1)),  # Ejemplo de límite mínimo
            MaxValueValidator(limit_value=date.today())  # Ejemplo de límite máximo
        ]
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

