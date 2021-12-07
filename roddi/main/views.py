import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.urls import reverse
from dodsbo.models import Dodsbo
from dodsbo.decorators import uautentisert_bruker, tillatte_brukere
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.template.loader import get_template
from main.models import Eiendel, Valg, Prioritering, Tildelt
from django.db.models import Q
from .forms import BrukerRegistreringForm
from .forms import EiendelForm, ValgForm, PrioriteringsForm, KommentarForm
from .forms import KontaktForm


def home(request):
    """Returnerer en render med request, index.html(forside) og
    informasjon om dødsbo.
    """

    alle_dodsbo = Dodsbo.objects.all()
    teller = 0
    teller_avsluttet = 0

    for dodsbo in alle_dodsbo:
        """Finner antall dødsbo, samt aktive dødsbo for brukeren."""
        if request.user in dodsbo.members.all():
            teller += 1
            if dodsbo.statusoppgjør == "AVSLUTTET":
                teller_avsluttet += 1

    teller_aktive = teller - teller_avsluttet

    innhold_data = {
        'teller': teller,
        'teller_aktive': teller_aktive,
        'teller_avsluttet': teller_avsluttet}

    return render(request, 'index.html', innhold_data)


def kontakt(request):
    """Funksjon for å ta kontakt med Røddi."""

    # Dersom man er i POST-modus og formen er godkjent,
    # vil det sendes en mail til Røddi.
    # Man blir deretter redirectet til kontakt-siden.
    if request.method == 'POST':
        form = KontaktForm(request.POST)

        if form.is_valid():
            fraemail = form.cleaned_data['fraemail']
            tittel = form.cleaned_data['tittel']
            tekst = form.cleaned_data['tekst']

        # Sender mailen
        send_mail(
            tittel,
            tekst,
            fraemail,
            ['mailroddi@gmail.com', fraemail],
        )

        # Generer suksess-melding
        messages.success(request, f'E-posten ble sendt!')

        return redirect('kontakt')

    # Dersom man ikke er i POST-modus.
    else:
        form = KontaktForm(request.POST)
        return render(request, 'kontakt.html', {'form': form})


# Restriksjon på views.dodsbos, må være logget inn.
@login_required(login_url='logginn')
# Tillatte brukergrupper.
@tillatte_brukere(tillatte_grupper=["admin"])
def dashboard(request):
    """Metode for dashboard.html """

    # Innholdet i dashbordet
    antall_dodsbo = Dodsbo.objects.all().count()
    antall_brukere = User.objects.all().count()
    antall_items = Eiendel.objects.all().count()
    antall_tildelt_items = Tildelt.objects.all().count()
    alle_brukere = User.objects.all()
    alle_dodsbo = Dodsbo.objects.all()

    # Finner datoer for ønsket tidsintervall
    idag = datetime.date.today()
    dager_7_siden = idag - datetime.timedelta(days=7)
    dager_30_siden = idag - datetime.timedelta(days=30)

    antall_nye_idag = User.objects.filter(date_joined__contains=idag).count()

    teller_7dager = 0
    teller_30dager = 0
    teller_aktive_dodsbo = 0
    teller_avsluttede_dodsbo = 0
    andel_tildelte_items = 0

    for bruker in alle_brukere:
        """Finner antall nye brukere siste 7 eller 30 dager"""

        if bruker.date_joined.date() > dager_30_siden:
            teller_30dager += 1
        if bruker.date_joined.date() > dager_7_siden:
            teller_7dager += 1

    for dodsbo in alle_dodsbo:
        """Finner alle avslutted dødsbo"""

        if dodsbo.statusoppgjør == "AVSLUTTET":
            teller_avsluttede_dodsbo += 1

    # Finner medlemmer til valgt dødsbo fra drop-down menyen
    aktuelt_dodsbo = None
    medlemmer = ""
    if request.method == "POST":
        index_dodsbo = request.POST.get("aktuell_dodsbo")
        if index_dodsbo is not None:
            aktuelt_dodsbo = alle_dodsbo[int(index_dodsbo) - 1]
            medlemmer = aktuelt_dodsbo.members.all()

    # Finner avsluttede dødsbo
    teller_aktive_dodsbo = antall_dodsbo - teller_avsluttede_dodsbo

    # Finner andel tidldelte gjenstander totalt
    andel_tildelte_items = int((antall_tildelt_items / antall_items) * 100)

    innhold_data = {
        'medlemmer': medlemmer,
        'aktuelt_dodsbo': aktuelt_dodsbo,
        'alle_dodsbo': alle_dodsbo,
        'antall_dodsbo': antall_dodsbo,
        'antall_brukere': antall_brukere,
        'antall_items': antall_items,
        'antall_nye_idag': antall_nye_idag,
        'teller_7dager': teller_7dager,
        'teller_30dager': teller_30dager,
        'teller_aktive_dodsbo': teller_aktive_dodsbo,
        teller_avsluttede_dodsbo: 'teller_avsluttede_dodsbo',
        'andel_tildelte_items': andel_tildelte_items}

    return render(request, "dashboard.html", innhold_data)


@uautentisert_bruker
def registrering(request):
    """Returnerer en redirect til logginn om skjemaet er gyldig.

    Hva som er på nettsidens side for brukerregistrering
    """

    # Hva som skjer når siden er i POST-modus (dvs. modusen når man har
    # trykket på "send inn")
    if request.method == 'POST':
        # setter skjemaet lik registreringsskjemaet for brukere definert i
        # forms.py
        form = BrukerRegistreringForm(request.POST)

        # Dersom skjemaet er gyldig lagres det.
        # Hvert skjema som sendes inn lagres så ikke duplikater oppstår senere.
        # Brukeren blir registert og det lagres en suksess-melding.
        # I tillegg får brukeren en velkomst-mail.
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Bruker laget for {username}!')
            name = form.cleaned_data.get('first_name')

            # Det sendes en mail til brukeren som registrerer seg.
            subject = 'Velkommen til Røddi'
            html_message = render_to_string('registrering_email.html')
            plain_message = strip_tags(html_message)
            email_from = settings.EMAIL_HOST_USER
            email_to = [form.cleaned_data.get('email')]
            send_mail(subject,
                      plain_message,
                      email_from,
                      email_to,
                      html_message=html_message)

            return redirect('logginn')

    # Hva som skjer når siden ikke er i POST-modus (dvs. når man går inn på
    # siden eller refresher siden)
    else:
        # Setter forms lik skjemaet for brukerregistrering (definert i
        # forms.py)
        form = BrukerRegistreringForm()

    # Viser brukerregistreringsskjemaet
    return render(request, 'registrering.html', {'form': form})


@uautentisert_bruker
def logginn(request):
    """Nettsidens side for innlogging av brukere"""

    # Hva som skjer når siden er i POST-modus (dvs. modusen når man har
    # trykket på "logg inn")
    if request.method == 'POST':
        # Brukernavn og passord lagres og sjekkes opp mot databasen
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        # Dersom innloggingsinfo samsvarer med en bruker i databsen
        # logges brukeren inn og blir tatt til hjemmesiden.
        if user is not None:
            auth.login(request, user)
            return redirect('/')

        # Dersom innloggingsinfo IKKE samsvarer med en bruker i
        # databsen produserer en feilmelding (error message)
        else:
            messages.error(request, "Feil brukernavn eller passord.")
            return HttpResponseRedirect(request.path_info)  # refresher siden

    else:
        # Peker på html-filen for forsiden
        return render(request, 'logginn.html')


def loggut(request):
    # Logger ut brukeren og tar den til hjemmesiden.
    auth.logout(request)
    return redirect('/')


def vis(request, name):
    """Tar inn en request og navn til et dødsbo.
    Returnerer alle gjenstandene i et dødsbo.
    Samt status på disse.
    """

    dodsbo = Dodsbo.objects.get(id=name)
    items = Eiendel.objects.filter(dodsbo=dodsbo)
    valg = Valg.objects.filter(item__in=items)

    # Søke/filtrerings logikk
    sokeord = None
    resultat_sjekk = False
    if request.method == 'POST':
        sokeord = request.POST.get("sokeord", None)
        if sokeord is not None:
            items = items.filter(
                Q(item_name__icontains=sokeord) |
                Q(item_desc__icontains=sokeord))

            if not items:
                resultat_sjekk = True
                print(resultat_sjekk)

    # Key er ID til item, value er enten antall brukere som har svart
    # eller hvem eiendelen har blitt tildelt til
    status = dict()

    for item in items:
        """Går gjennom alle eiendeler i et dødsbo og teller antall
        brukere som har gjort et valg."""

        counter = 0
        brukere = dodsbo.members.all()

        # Henter tildelingen hvis det er blitt gjort
        try:
            tildeling = Tildelt.objects.get(eiendel_id=item.id)
            status[item.id] = "Tildelt til " + str(tildeling.user)

        # Ellers vises bare hvor mange som har svart
        except Tildelt.DoesNotExist:
            for bruker in brukere:
                # Hvis en bruker har lagt inn et ønske, inkrementeres counter
                if Valg.objects.filter(
                        item_id=item.id,
                        user_id=bruker).exists():
                    counter += 1
            # Legger til i dictionary
            status[item.id] = str(counter) + " av " + \
                str(brukere.count()-1) + " har svart"

    return render(request,
                  "vis.html",
                  {'status': status,
                   'items': items,
                   'sokeord': sokeord,
                   'resultat_sjekk': resultat_sjekk})


def lagre_valg(request, item_name):
    """Returnerer valg, kommentar og prioritering gjort på en eiendel

    Tar inn navnet på en gjenstand.
    """

    item = Eiendel.objects.get(id=item_name)
    valg = Valg.objects.all()
    if request.method == "POST":
        form_prioritering = PrioriteringsForm(request.POST)
        form = ValgForm(request.POST)
        if form.is_valid():
            try:
                Valg.objects.filter(
                    user_id=request.user.id,
                    item_id=item_name).delete()  # Sletter tidligere valg
            except Prioritering.DoesNotExist:
                pass
            form.save()
            messages.success(request, f'Valg oppdatert')
        if form_prioritering.is_valid():
            # Try/catch: ser om prioritering allerede ligger inne, og sletter
            # om nødvendig
            try:
                prio = Prioritering.objects.filter(
                    userprio=request.user).get(
                    itemprio=item)
                prio.delete()
            except Prioritering.DoesNotExist:
                prio = None

            # Henter info fra requesten
            userprio = request.user
            choiceprio = request.POST.get('PrioriteringsValget')
            # Lagrer prioriteringen i DB
            prio = Prioritering.objects.create(
                userprio=userprio, itemprio=item, PrioriteringsValget=choiceprio)

            messages.success(request, f'Prioritering lagret')
    else:
        form_prioritering = PrioriteringsForm()
        form = ValgForm()

    # Deklarer all_prio som prioriteringstabellen fra databasen
    all_prio = Prioritering.objects.filter(itemprio=item)
    eiendel = Eiendel.objects.get(id=item_name)
    kommentarer = eiendel.kommentarer.filter(aktiv=True)
    kommentar_avventer = eiendel.kommentarer.filter(aktiv=False)
    ny_kommentar = None

    if request.method == 'POST':
        kommentar_form = KommentarForm(data=request.POST)
        if kommentar_form.is_valid():
            ny_kommentar = kommentar_form.save(commit=False)
            ny_kommentar.eiendel = eiendel
            ny_kommentar.save()
    else:
        kommentar_form = KommentarForm()

    try:
        tildeling = Tildelt.objects.get(eiendel_id=item.id)
    except Tildelt.DoesNotExist:
        tildeling = None

    return render(request,
                  "eiendel.html",
                  {'item': item,
                   'form': form,
                   'eiendel': eiendel,
                   'Valg': valg,
                   'kommentarer': kommentarer,
                   'kommentar_avventer': kommentar_avventer,
                   'ny_kommentar': ny_kommentar,
                   'kommentar_form': kommentar_form,
                   'Prioritering': all_prio,
                   'Tildeling': tildeling})


def eiendel_detaljer(request, eiendel):
    """Tar inn en eiendel og returnerer detaljer om den.
    Returnerer også kommentarer gjort på en eiendel.
    """

    eiendel = get_object_or_404(Eiendel, slug=eiendel)
    kommentarer = eiendel.kommentarer.filter(aktiv=True)
    ny_kommentar = None

    if request.method == 'POST':
        kommentar_form = KommentarForm(data=request.POST)
        if kommentar_form.is_valid():
            ny_kommentar = kommentar_form.save(commit=False)
            ny_kommentar.eiendel = eiendel
            ny_kommentar.save()
    else:
        kommentar_form = KommentarForm()

    return render(request, 'eiendel.html', {'eiendel': eiendel,
                                            'kommentarer': kommentarer,
                                            'ny_kommentar': ny_kommentar,
                                            'kommentar_form': kommentar_form})


def tildeling(request, id):
    # Henter eiendelen som vi har klikket oss inn på
    eiendel = Eiendel.objects.get(id=id)
    # Henter dodsboet som eiendelen er tilegnet
    dodsbo = Dodsbo.objects.get(id=eiendel.dodsbo.id)
    # Henter alle valg/kommentarer som er til denne eiendelen
    valg = Valg.objects.filter(item=eiendel)
    # Henter alle prioriteringer som er til denne eiendelen
    prioritering = Prioritering.objects.filter(itemprio=eiendel)
    # Henter tildeling knyttet til denne eiendelen
    tildeling = Tildelt.objects.filter(eiendel=eiendel)

    if request.method == 'POST':
        bruker_id = request.POST['user']
        bruker = User.objects.get(id=bruker_id)
        Tildelt.objects.create(user=bruker, eiendel=eiendel)

    return render(request, "tildeling.html",
                  {
                      'Eiendel': eiendel,
                      'Dodsbo': dodsbo,
                      'Valg': valg,
                      'Prioritering': prioritering,
                      'Tildeling': tildeling
                  }
                  )
