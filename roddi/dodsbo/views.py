from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import tillatte_brukere
from .models import Dodsbo
from .forms import AddMemberToDodsboForm


# Restriksjon på views.dodsbos. Bruker må være logget inn.
@login_required(login_url="logginn")
def dodsbos(request):
    """Returnerer en liste med alle dødsbo"""

    if request.method == "POST":
        form = AddMemberToDodsboForm(request)
        # Sjekker om form er valid
        # Henter først id-feltet fra requesten
        # Deretter finner en riktig dødsbo fra databasen
        # Så legges en bruker til
        # Til slutt lagres dødsboet
        if form.is_valid():
            dodsbosid = request.POST["id"]
            dodsbo = Dodsbo.objects.get(pk=dodsbosid)
            dodsbo.members.add(request.user)
            dodsbo.save()

    all_dodsbos = Dodsbo.objects.all()

    return render(request, "dodsbos.html", {"Dodsbos": all_dodsbos})
