from django.contrib import admin
from .models import Prioritering, Eiendel, Kommentar, Tildelt, Valg
from dodsbo.models import Dodsbo


@admin.register(Eiendel)
class EiendelAdmin(admin.ModelAdmin):
    """
    Registrering av Eiendel til adminpanel. I tillegg er det mulig å filtere
    eiendeler etter hvilket dødsbo det hører til.
    """

    # list_display bestemmer hvordan modellen vises i admin-panelet
    # list_filter gir admin mulighet til å filtrere
    list_display = ('item_name', 'dodsbo')
    list_filter = ('dodsbo', 'item_name')


@admin.register(Kommentar)
class CommentAdmin(admin.ModelAdmin):
    """
    Registrering av Kommentar til adminpanel. I tillegg er det mulig å
    filtere kommentarer etter status(aktiv/ikke aktiv), datoen de er
    laget og hvilket dødsbo de hører til.
    """

    # list_display bestemmer hvordan modellen vises i admin-panelet
    # list_filter gir admin mulighet til å filtrere
    # actions gir admin mulighet til å godta en kommentar
    list_display = ('user', 'kommentar', 'eiendel', 'dato_laget', 'aktiv')
    list_filter = ('aktiv', 'dato_laget')
    actions = ['godta_kommentar']

    def godta_kommentar(self, request, queryset):
        """Funksjon som lar admin godkjenne en kommentar."""

        queryset.update(aktiv=True)


admin.site.register(Tildelt)
