from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='i_gruppe')
def i_gruppe(user, gruppe_navn): 
    """
    Returnerer True dersom user er medlem i gruppe med gruppe_navn som navn
    """
    group = Group.objects.get(name=gruppe_navn) 
    return True if group in user.groups.all() else False