from django.urls import path

from .views import index

app_name = "wallet"
urlpatterns = [
    path("", index, name="index"),
]
