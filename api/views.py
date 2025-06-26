# api/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Pagamento, Categoria
from .serializers import PagamentoSerializer, CategoriaSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class PagamentoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PagamentoSerializer

    def get_queryset(self):
        # Retorna apenas os pagamentos do usuário logado
        return Pagamento.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        # Associa o pagamento ao usuário logado ao criar
        serializer.save(usuario=self.request.user)