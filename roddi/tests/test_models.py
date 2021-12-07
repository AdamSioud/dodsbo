from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from main.models import Eiendel, Prioritering
from dodsbo.models import Dodsbo

# Kan kjøres ved python manage.py test tests
# om man er i roddi mappe


class EiendelTest(TestCase):
    """
    Tester Eiendelsmodellen opp mot databasen
    """

    def setUp(self):
        dodsbo1 = Dodsbo.objects.create(
            name="Leilighet i sentrum",
            descritption="Slitt og rar lukt")
        Eiendel.objects.create(item_name="Lenestol",
                               item_desc="Godt slitt",
                               item_choice="K",
                               dodsbo=dodsbo1)

    def test_set_up(self):
        """
        Tester om man kan hente eiendelene i databasen
        """
        lenestol = Eiendel.objects.get(item_name="Lenestol")
        self.assertEqual(lenestol.item_desc, "Godt slitt")
        self.assertEqual(lenestol.item_choice, "K")

    def check_lenght_name(self):
        """
        Sjekker om man får navn
        """
        lenestol = Eiendel.objects.get(item_name="Lenestol")
        self.assertEqual(lenestol.item_names, "Lenestol")


class DodsboTest(TestCase):
    """
    Tester Dodsbomodellen opp mot databasen
    """

    def create_and_login(self, username, password):
        """
        Hjelpemetode for testene
        Metode for å automatisk lage og logge inn bruker
        """
        user1 = User.objects.create_user(username, password)
        self.client.login(username=username, password=password)
        return user1

    def setUp(self):
        self.user = self.create_and_login(
            username='testuser', password='1a2b3c4d')
        """ User.objects.create_user(username='testuser', password='1a2b3c4d')
        self.client.login(username='testuser', password='1a2b3c4d') """
        Dodsbo.objects.create(
            name="Leilighet i sentrum",
            descritption="Slitt og rar lukt")
        dodsboA = Dodsbo.objects.create(
            name="Fortet", descritption="Etter onkelen fra Amerika")
        dodsboA.members.add(self.user)

    def test_add_member(self):
        """
        Sjekker medlems feltet
        """
        dodsbo1 = Dodsbo.objects.get(name="Leilighet i sentrum")
        dodsbo1.members.add(self.user)
        self.assertTrue(self.user in dodsbo1.members.all())

        dodsbo2 = Dodsbo.objects.get(name="Fortet")
        user2 = self.create_and_login('testuser2', '5e6f7g8h')
        dodsbo2.members.add(user2)
        self.assertTrue(user2 in dodsbo2.members.all())

        self.assertFalse(user2 in dodsbo1.members.all())


class PrioriteringTest(TestCase):
    """
    Tester Prioriteringsmodellen opp mot databasen
    """

    def setUp(self):
        dodsbo1 = Dodsbo.objects.create(
            name="Leilighet i sentrum",
            descritption="Slitt og rar lukt")
        Eiendel.objects.create(item_name="Lenestol",
                               item_desc="Godt slitt",
                               item_choice="K",
                               dodsbo=dodsbo1)
        self.user = User.objects.create_user(
            username='testuser', password='1a2b3c4d')
        self.client.login(username='testuser', password='1a2b3c4d')
        dodsbo1.members.add(self.user)

    def test_prio(self):
        """
        Tester ulike aspekter ved kobling mellom prioritetsobjekt og databasen
        """
        eiendel = Eiendel.objects.get(item_name='lenestol')
        try:
            Prioritering.objects.filter(
                userprio=self.user).get(
                itemprio=eiendel)
            self.fail(
                msg='Feilet ikke da hentet prioritering som ikke eksisterer')
        except Prioritering.DoesNotExist:
            try:
                Prioritering.objects.create(
                    PrioriteringsValget='3',
                    userprio=self.user,
                    itemprio=eiendel)
                prio = Prioritering.objects.filter(
                    userprio=self.user).get(
                    itemprio=eiendel)
                prio.delete()
                try:
                    Prioritering.objects.filter(
                        userprio=self.user).get(
                        itemprio=eiendel)
                    self.fail('Klarte å hente objekt etter sletting')
                except Prioritering.DoesNotExist:
                    pass
            except Prioritering.DoesNotExist:
                self.fail('Feilet i å hente eksisterende eiendel')
            except BaseException:
                self.fail()

    def test_ny_prio_ved_eksisterende(self):
        eiendel = Eiendel.objects.get(item_name='lenestol')
        Prioritering.objects.create(
            PrioriteringsValget='3',
            userprio=self.user,
            itemprio=eiendel)
        try:
            Prioritering.objects.create(
                PrioriteringsValget='5',
                userprio=self.user,
                itemprio=eiendel)
            fail(
                'Skal ikke kunne være to prioriteringer tilknyttet samme eiendel og person')
        except IntegrityError:
            pass
        except BaseException:
            self.fail()
