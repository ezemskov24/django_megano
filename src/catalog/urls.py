from django.urls import path

from .views import (
    show_review,
)

app_name = "catalog"

urlpatterns = [
    path("add/", show_review, name="show_review"),
]
