# notas/views.py
from rest_framework import viewsets
from .models import Nota
from .serializers import NotaSerializer

class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
