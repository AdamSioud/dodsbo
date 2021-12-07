from django.urls import path
from . import views

urlpatterns = [
    path("", views.dodsbos, name="dodsbo"),
]
