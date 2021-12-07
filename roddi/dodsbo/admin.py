from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from .mail_admin import send_mail, send_welcome, send_reminder, send_closed
from .models import Dodsbo
from main.models import Eiendel, Valg


class ChoiceInline(admin.TabularInline):
    """Klasse for å gi admin mulighet til å legge inn eiendeler når
    det opprettes et dødsbo.
    """

    model = Eiendel
    extra = 3


@admin.register(Dodsbo)
class DodsboAdmin(admin.ModelAdmin):
    """Registrerer et dødsbo til admin-panelet.

    Inlines bruker ChoiceInline, som gir admin mulighet til å legge
    inn eiendeler.

    Actions gir admin mulighet til å sende varslinger(sende mail) til
    brukere.
    """

    fieldsets = [
        (
            None,
            {"fields": 
                ["name", "image", "descritption", "statusoppgjør", "members"]
            },
        )
    ]
    inlines = [ChoiceInline]
    actions = [send_welcome, send_reminder, send_closed]
