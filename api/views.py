# api/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import HttpResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from .models import Pagamento, Categoria, Cliente
from .serializers import PagamentoSerializer, CategoriaSerializer, ClienteSerializer

# --- Função Auxiliar Chave ---
def get_cliente_from_request(request):
    user = request.user
    if user.is_superuser and request.headers.get('X-Cliente-Gerenciado-Id'):
        try:
            cliente_id = int(request.headers.get('X-Cliente-Gerenciado-Id'))
            return Cliente.objects.get(id=cliente_id)
        except (ValueError, Cliente.DoesNotExist):
            return user.perfilusuario.cliente
    return user.perfilusuario.cliente

# --- Viewsets Principais ---
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

    def get_queryset(self):
        cliente = get_cliente_from_request(self.request)
        return Pagamento.objects.filter(cliente=cliente)

    def perform_create(self, serializer):
        cliente = get_cliente_from_request(self.request)
        serializer.context['request'] = self.request
        serializer.save(cliente=cliente)
    
    def get_serializer_context(self):
        return {'request': self.request}

# --- Viewset do Admin ---
class ClienteAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cliente.objects.all().order_by('nome_empresa')
    serializer_class = ClienteSerializer
    permission_classes = [IsAdminUser]

# --- View de Perfil do Usuário ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_superuser': user.is_superuser,
        'cliente_id': user.perfilusuario.cliente.id if hasattr(user, 'perfilusuario') else None
    }
    return Response(data)

# --- NOVA VIEW PARA GERAÇÃO DE RELATÓRIO PDF ---
class GerarRelatorioPDF(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        cliente = get_cliente_from_request(request)
        
        data_inicio = request.data.get('data_inicio')
        data_fim = request.data.get('data_fim')
        
        if not data_inicio or not data_fim:
            return Response({"error": "Datas de início e fim são obrigatórias."}, status=status.HTTP_400_BAD_REQUEST)
        
        pagamentos = Pagamento.objects.filter(
            cliente=cliente,
            data_competencia__range=[data_inicio, data_fim]
        ).order_by('data_competencia')

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # --- Desenhando o PDF ---
        p.setFont("Helvetica-Bold", 16)
        p.drawString(inch, height - inch, f"Relatório de Pagamentos")
        p.setFont("Helvetica", 12)
        p.drawString(inch, height - 1.2*inch, f"Cliente: {cliente.nome_empresa}")
        p.drawString(inch, height - 1.4*inch, f"Período de Competência: {data_inicio} a {data_fim}")
        
        y = height - 2.2*inch
        p.setFont("Helvetica-Bold", 10)
        p.drawString(inch, y, "Competência")
        p.drawString(2*inch, y, "Descrição")
        p.drawString(5*inch, y, "Categoria")
        p.drawString(6.5*inch, y, "Valor (R$)")
        y -= 15
        p.line(inch, y, width - inch, y)
        y -= 20

        p.setFont("Helvetica", 10)
        total = 0
        for pg in pagamentos:
            if y < inch: # Page break
                p.showPage()
                y = height - inch
                p.setFont("Helvetica", 10)

            p.drawString(inch, y, pg.data_competencia.strftime('%d/%m/%Y'))
            p.drawString(2*inch, y, pg.descricao[:40])
            p.drawString(5*inch, y, pg.categoria.nome if pg.categoria else 'N/A')
            valor_str = f"{pg.valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            p.drawRightString(width - inch, y, valor_str)
            total += pg.valor
            y -= 20
        
        y -= 10
        p.line(inch, y, width - inch, y)
        y -= 20
        p.setFont("Helvetica-Bold", 12)
        p.drawString(5*inch, y, "Total do Período:")
        total_str = f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        p.drawRightString(width - inch, y, total_str)
        
        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_pagamentos.pdf"'
        
        return response