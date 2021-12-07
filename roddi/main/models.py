from django.db import models
from django.forms import forms
from django.db import connections
from django.contrib.auth.models import User
from dodsbo.models import Dodsbo


ITEM_CHOICES = (
    ('K', 'Behold'),
    ('D', 'Doner'),
    ('T', 'Kast'),
)


class Eiendel(models.Model):
    """ En klasse for eiendeler. Hver eiendel hører til et dødsbo. """

    # Eiendelen blir koblet til et dødsbo som er en fremmednøkkel.
    dodsbo = models.ForeignKey(Dodsbo,
                               on_delete=models.CASCADE,
                               verbose_name="Dødsbo")
    item_name = models.CharField(max_length=30, verbose_name="Navn")
    item_desc = models.CharField(max_length=300, verbose_name="Beskrivelse")
    item_image = models.ImageField(blank=0, null=True, verbose_name="Bilde")
    item_choice = models.CharField(max_length=1,
                                   choices=ITEM_CHOICES,
                                   default='K', verbose_name="Valg")

    def __str__(self):
        """ Representerer klassens objekter på gjenstanden sitt navn. """

        return self.item_name

    class Meta:

        db_table = "items"

        # Endrer visning av navn i entall og flertalls form
        verbose_name = 'Eiendel'
        verbose_name_plural = 'Eiendeler'


class Valg(models.Model):
    """ En klasse for valg.
    Hvert valg hører til en eiendel og en bruker.
    """

    choice = models.CharField(max_length=1, choices=ITEM_CHOICES,
                              default='K', verbose_name="Valg")
    comment = models.CharField(max_length=200, verbose_name="Kommentar")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             default=1, verbose_name="Bruker")
    item = models.ForeignKey(Eiendel, on_delete=models.CASCADE,
                             default=1, verbose_name="Eiendel")

    def __str__(self):
        return self.choice

    def get_valg(self):
        """Returnerer valget"""

        valg_dict = {
            'K': 'Behold',
            'D': 'Doner',
            'T': 'Kast'
        }
        return valg_dict.get(self.choice)

    class Meta:
        db_table = "item_choice"

        # Endrer visning av navn i entall og flertalls form
        verbose_name = 'Valg'
        verbose_name_plural = 'Valg'


# De ulike prioriteringene en bruker kan gi på en eiendel
Prioritering_alternativ = (
    ('1', 'Ikke viktig'),
    ('2', 'Litt viktig'),
    ('3', 'Interessert'),
    ('4', 'Ganske interessert'),
    ('5', 'Veldig interessert')
)


class Prioritering(models.Model):
    """ En klasse for prioritering.
    Hver prioritering hører til en eiendel og en bruker.
    """

    PrioriteringsValget = models.CharField(max_length=1,
                                           choices=Prioritering_alternativ,
                                           default='1',
                                           verbose_name="Prioritering")
    userprio = models.ForeignKey(User, on_delete=models.CASCADE,
                                 default=1, verbose_name="Bruker")
    itemprio = models.ForeignKey(Eiendel, on_delete=models.CASCADE,
                                 default=1, verbose_name="Eiendel")

    def __str__(self):
        streng = 'Bruker:'
        streng += self.userprio.__str__()
        streng += ' |Eiendel:'
        streng += self.itemprio.__str__()
        return streng

    def get_valg(self):
        prio_dict = {
            '1': 'Ikke viktig',
            '2': 'Litt viktig',
            '3': 'Interessert',
            '4': 'Ganske interessert',
            '5': 'Veldig interessert'
        }
        return prio_dict.get(self.PrioriteringsValget)

    class Meta:
        db_table = "prioritering"

        # Sammensatt nøkkel
        unique_together = (('userprio', 'itemprio'),)

        # Endrer visning av navn i entall og flertalls form
        verbose_name = 'Prioritering'
        verbose_name_plural = 'Prioriteringer'


class Kommentar(models.Model):
    """
    En klasse for kommentarer. Hver kommentar hører til et en bruker og
    en gitt eiendel. Før en kommentar blir vist må den godkjennes av admin.
    """

    # Fremmednøkkel til Eiendel - kommentar til en gitt eiendel
    eiendel = models.ForeignKey(Eiendel,
                                on_delete=models.CASCADE,
                                related_name='kommentarer')

    # Brukeren som kommenterer, default er admin ettersom man må ha en default
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             default=1,
                             verbose_name="Bruker")

    kommentar = models.TextField()
    dato_laget = models.DateTimeField(auto_now_add=True)

    # admin må godkjenne en kommentar før den er blir satt til aktiv
    aktiv = models.BooleanField(default=False)

    class Meta:
        """ Sortering skjer på datoen kommentaren er laget. """
        ordering = ['dato_laget']

        # Endrer visning av navn i entall og flertalls form
        verbose_name = 'Kommentar'
        verbose_name_plural = 'Kommentarer'

    def __str__(self):
        """ Representerer klassens objekter med innholdet i kommentaren
        og bruker sitt navn.
        """
        return 'Kommentar {} av {}'.format(self.kommentar, self.user)


class Tildelt(models.Model):
    """
    Modell for å lagre tildeling av eiendeler
    """
    eiendel = models.ForeignKey(Eiendel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """ Representerer klassens objekter med eiendel
        og bruker sitt navn.
        """
        return '{} er blitt tildelt til {} i dødsboet: {}'.format(
            self.eiendel, self.user, self.eiendel.dodsbo)

    class Meta:
        # Endrer visning av flertalls form
        verbose_name_plural = 'Tildelt'
