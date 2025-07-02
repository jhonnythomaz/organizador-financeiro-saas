# api/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum, Q

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from django_filters.rest_framework import DjangoFilterBackend

from .models import Pagamento, Categoria, Cliente, PerfilUsuario
from .serializers import PagamentoSerializer, CategoriaSerializer, ClienteSerializer, UserSerializer
from .filters import PagamentoFilter

# --- Função Auxiliar ---
def get_cliente_from_request(request):
    user = request.user
    if user.is_superuser and request.headers.get('X-Cliente-Gerenciado-Id'):
        try:
            cliente_id = int(request.headers.get('X-Cliente-Gerenciado-Id'))
            return Cliente.objects.get(id=cliente_id)
        except (ValueError, Cliente.DoesNotExist):
            return user.perfilusuario.cliente
    return user.perfilusuario.cliente

# --- Viewsets ---
class CategoriaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriaSerializer

    def get_queryset(self):
        cliente = get_cliente_from_request(self.request)
        return Categoria.objects.filter(cliente=cliente)

    def perform_create(self, serializer):
        cliente = get_cliente_from_request(self.request)
        serializer.context['request'] = self.request 
        serializer.save(cliente=cliente)
        
    def get_serializer_context(self):
        return {'request': self.request}

class PagamentoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PagamentoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PagamentoFilter

    def get_queryset(self):
        cliente = get_cliente_from_request(self.request)
        return Pagamento.objects.filter(cliente=cliente)

    def perform_create(self, serializer):
        cliente = get_cliente_from_request(self.request)
        serializer.context['request'] = self.request
        serializer.save(cliente=cliente)
    
    def get_serializer_context(self):
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        agregados = queryset.aggregate(
            total_pago=Sum('valor', filter=Q(status='Pago')),
            total_pendente=Sum('valor', filter=Q(status='Pendente', data_vencimento__gte=timezone.now().date())),
            total_atrasado=Sum('valor', filter=Q(status='Pendente', data_vencimento__lt=timezone.now().date())),
        )
        
        serializer = self.get_serializer(queryset, many=True)
        response_data = {
            'pagamentos': serializer.data,
            'totais': {
                'pago': agregados.get('total_pago') or 0,
                'pendente': agregados.get('total_pendente') or 0,
                'atrasado': agregados.get('total_atrasado') or 0,
            }
        }
        return Response(response_data)

    # --- CORREÇÃO: Sobrescrevendo métodos para retornar a lista atualizada ---
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        # Retorna status 200 OK com a lista atualizada, em vez de 204 No Content
        return self.list(request, *args, **kwargs)

class ClienteAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminUser]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    perfil = getattr(user, 'perfilusuario', None)
    if perfil:
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_superuser': user.is_superuser,
            'cliente_id': perfil.cliente.id,
            'cliente_nome': perfil.cliente.nome_empresa,
        })
    return Response({'detail': 'Perfil não encontrado.'}, status=404)

class GerarRelatorioPDF(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Implemente aqui a geração do PDF conforme sua lógica
        return Response({'detail': 'Relatório gerado (mock).'})