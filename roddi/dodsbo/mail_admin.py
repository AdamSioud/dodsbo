from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from .models import Dodsbo
from main.models import Eiendel
from main.models import Valg


def send_welcome(self, request, queryset):
    """Funksjon for å sende en velkomst-varsling til brukere i et dødsbo.
    Hver bruker får en mail med informasjon om hvordan oppgjøret fungerer.

    I tillegg blir statusoppgjør satt til PÅGÅR.
    """

    queryset.update(statusoppgjør="PÅGÅR")

    # Innholdet i mailen og hvem mailen er fra.
    # Innholdet er hentet fra en html-fil.
    subject = "Registrert i dødsbo"
    html_message = render_to_string("velkommen_email.html")
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER

    # Her bestemmes hvem som mottar mailen.
    for dodsbo in queryset:
        """Løkke som finner det aktuelle dødsboet"""
        for member in (dodsbo.members.all()):
            """Løkke som sender mail til hvert medlem av dødsboet."""

            # send_mail er en importert funksjon fra django.core.mail
            # biblioteket.
            send_mail(subject,
                      plain_message,
                      email_from,
                      [member.email],
                      html_message=html_message)


# Beskrivelse av hva funksjonen gjør i admin-panelet
send_welcome.short_description = "Send velkommen-email til alle i dødsboet"


def send_reminder(self, request, queryset):
    """Funksjon for å sende en påminnelse-varsling til brukere i et
    dødsbo. Når det nærmer seg fristen for å velge kan admin sende ut en
    påminnelse til alle brukerene. Dette for å minne de på å prioritere.

    I tillegg blir statusoppgjør satt til ENUKEIGJEN.
    """

    # Innholdet i mailen og hvem mailen er fra.
    # Innholdet er hentet fra en html-fil.
    subject = "Frist på dødsbo går snart ut"
    html_message = render_to_string("påminnelse_email.html")
    plain_message = strip_tags(html_message)
    queryset.update(statusoppgjør="ENUKEIGJEN")
    email_from = settings.EMAIL_HOST_USER

    for dodsbo in queryset:
        """Løkke som finner det aktuelle dødsboet"""
        for member in (dodsbo.members.all()):
            """Løkke som sender mail til hvert medlem av dødsboet."""

            # send_mail er en importert funksjon fra django.core.mail
            # biblioteket.
            send_mail(subject,
                      plain_message,
                      email_from,
                      [member.email],
                      html_message=html_message)


# Beskrivelse av hva funksjonen gjør i admin-panelet
send_reminder.short_description = "Send påminnelse til alle i dødsboet"


def send_closed(self, request, queryset):
    """Funksjon for å sende en påminnelse-varsling til brukere i et dødsbo.
    Når det fristen for å velge er ute kan admin sende ut en påminnelse til
    alle brukerene. Dette for å informere om at det ikke lenger er mulig å
    velge.

    I tillegg blir statusoppgjør satt til AVSLUTTET.
    """

    # Innholdet i mailen og hvem mailen er fra.
    # Innholdet er hentet fra en html-fil.
    subject = "Frist på dødsbo er ute"
    html_message = render_to_string("avsluttet_email.html")
    plain_message = strip_tags(html_message)
    queryset.update(statusoppgjør="AVSLUTTET")
    email_from = settings.EMAIL_HOST_USER

    for dodsbo in queryset:
        """Løkke som finner det aktuelle dødsboet"""
        for member in (dodsbo.members.all()):
            """Løkke som sender mail til hvert medlem av dødsboet."""

            # send_mail er en importert funksjon fra django.core.mail
            # biblioteket.
            send_mail(subject,
                      plain_message,
                      email_from,
                      [member.email],
                      html_message=html_message)


# Beskrivelse av hva funksjonen gjør i admin-panelet
send_closed.short_description = "Send avsluttet til alle i dødsboet"
