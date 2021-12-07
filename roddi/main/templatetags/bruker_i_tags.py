from django import template
from main.models import Valg, Prioritering
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name='brukers_valg')
def brukers_valg(Valg, brukerID):
    """
    Returnerer True dersom bruker har et valg som eksisterer i qureysetet Valg
    """
    bruker = User.objects.get(id = brukerID)
    for valg in Valg:
        if valg.user == bruker:
            return True
    return False

@register.filter(name='brukers_prio')
def brukers_prio(Prioiteringer, brukerID):
    """
    Returnerer True dersom bruker har et valg som eksisterer i qureysetet Prioiteringer
    """
    for prio in Prioiteringer:
        if prio.userprio.id == brukerID:
            return True
    return False

