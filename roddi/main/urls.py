from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    # Oppretter URL-er for nettsiden og kobler det opp mot views.py

    # URL for nettsidens forside (home)
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    # URL for kontakt-siden
    path('kontakt/', views.kontakt, name='kontakt'),
    # URL for nettsidens side for registrering (/registrering)
    path('registrering/', views.registrering, name='registrering'),
    # URL for nettsidens side for innlogging (/logginn)
    path('logginn/', views.logginn, name='logginn'),
    # URL for når brukeren logger ut
    path('loggut/', views.loggut, name='loggut'),
    # URL for å vise gjenstander
    path('dodsbo/<str:name>/', views.vis, name='dodsbo'),
    # URL for lagring og visning av valg og kommentarer
    path('vis/<str:item_name>/', views.lagre_valg, name='vis'),
    # URL for statussiden for til eiendel
    path('tildeling/<str:id>/', views.tildeling, name='tildeling')
]