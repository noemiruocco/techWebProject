from django.urls import path
from landingPage.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
]
