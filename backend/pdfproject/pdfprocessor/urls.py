from django.urls import path
from .views import processView

app_name="pdfprocessor"

urlpatterns = [
    path('process',processView.as_view(),name="process"),
]