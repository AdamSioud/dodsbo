from django.http import HttpResponse
from django.shortcuts import redirect


def uautentisert_bruker(input_funksjon):
    """Returnerer wrap-funksjonen (wrap kalles). Tar funksjonen som skal
    sjekkes som parameter.

    Decorator for å sjekke om bruker er logget inn.
    """

    def wrap(request, *args, **kwargs):
        """Redirecter til 'home' dersom bruker er innlogget.

        Returnerer opprinnelig funksjon viss ikke.
        """

        if request.user.is_authenticated:
            return redirect("home")
        else:
            return input_funksjon(request, *args, **kwargs)

    return wrap


def tillatte_brukere(tillatte_grupper=[]):
    """Returnerer funksjonen decorator. Input er en liste med
    tilatte brukere.
    """

    def decorator(input_funksjon):
        """Returnerer wrap-funksjonen.

        view_func er metoden vi ønsker å "sjekke"
        """

        def wrap(request, *args, **kwargs):
            """Gir bruker tilgang dersom han er med i en tillatt gruppe.
            Returerer HttpResponse viss ikke.
            """

            gruppe = None
            if request.user.groups.exists():
                gruppe = request.user.groups.all()[0].name

            if gruppe in tillatte_grupper: 
                return input_funksjon(request, *args, **kwargs)
            else:
                return HttpResponse("Du har ikke tilgang")

        return wrap

    return decorator
