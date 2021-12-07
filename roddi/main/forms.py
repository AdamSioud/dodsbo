from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Eiendel, Valg, Kommentar, Prioritering


class BrukerRegistreringForm(UserCreationForm):
    """Skjema for brukerregistrering.

    Lager en spesialisering av Django sin UserCreationForm.
    """

    # Tekstfelter for alle inputs (må ha engelsk variabelnavn pga. django)
    first_name = forms.CharField(label='Fornavn')
    last_name = forms.CharField(label='Etternavn')
    username = forms.CharField(label='Brukernavn')
    email = forms.EmailField(label='E-postadresse')
    password1 = forms.PasswordInput()

    # Check-box for aldersbekreftelse
    age_box = forms.BooleanField(
        required=True,
        label='Jeg bekrefter herved at jeg har fylt minimum 18 år')

    # Spesifiserer hvilket skjema som blir endret
    # og hvilke fields som skal utgjøre skjemaet
    class Meta:
        model = User
        # password2 er validering av passord1
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2']


class KontaktForm(forms.Form):
    """Skjema for å sende inn mail på kontakt.html"""

    fraemail = forms.EmailField(label="Din e-post")
    tittel = forms.CharField(label="Tittel")
    tekst = forms.CharField(
        widget=forms.Textarea,
        label="Skriv din melding her...")


class EiendelForm(forms.ModelForm):
    """Skjema for å legge inn en eiendel"""
    class Meta:
        model = Eiendel
        fields = ['item_name', 'item_desc', 'item_image']


class ValgForm(forms.ModelForm):
    """Skjema for å legge inn et valg"""
    class Meta:
        model = Valg
        fields = ['choice', 'comment', 'user', 'item']


class KommentarForm(forms.ModelForm):
    """Skjema for å legge inn en kommentar"""
    class Meta:
        model = Kommentar
        fields = ['user', 'kommentar']


class PrioriteringsForm(forms.ModelForm):
    """Skjema for å velge prioritering"""
    class Meta:
        model = Prioritering
        # Referer til field i modellen prioritering
        fields = ['PrioriteringsValget']
