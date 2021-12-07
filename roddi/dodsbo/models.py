from django.db import models
from django.forms import forms
from django.db import connections
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail


# De ulike statusene et dødsbo kan ha
STATUSOPPGJØR_CHOICES = (
    ("PÅGÅR", "Pågår"),
    ("ENUKEIGJEN", "En uke igjen"),
    ("AVSLUTTET", "Avsluttet"),
)


class Dodsbo(models.Model):
    """Klasse for et dødsbo.

    Består av navn, bilde, beskrivelse, status og et antall medlemmer.
    """

    name = models.CharField(max_length=50,
                            verbose_name="Navn")
    image = models.ImageField(upload_to="pics",
                              null=True,
                              verbose_name="Bilde")
    descritption = models.TextField(verbose_name="Beskrivelse")
    statusoppgjør = models.CharField(max_length=10,
                                     choices=STATUSOPPGJØR_CHOICES,
                                     default="PÅGÅR")

    # I DB vil dette lage egen tabell, dodsbo_members
    # Setter relasjon til items i items-class med ForeignKey
    members = models.ManyToManyField(User,
                                     default=None,
                                     verbose_name="Brukere")

    class Meta:
        # Endrer visning av navn i entall og flertalls form
        verbose_name = "Dødsbo"
        verbose_name_plural = "Dødsbo"

    def __str__(self):
        return self.name
