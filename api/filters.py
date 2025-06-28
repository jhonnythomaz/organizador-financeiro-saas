# api/filters.py
import django_filters
from .models import Pagamento

class PagamentoFilter(django_filters.FilterSet):
    # Filtro por intervalo de data de competência
    data_competencia_inicio = django_filters.DateFilter(field_name="data_competencia", lookup_expr='gte')
    data_competencia_fim = django_filters.DateFilter(field_name="data_competencia", lookup_expr='lte')
    
    # Filtro por descrição (case-insensitive)
    descricao = django_filters.CharFilter(field_name='descricao', lookup_expr='icontains')

    # Filtro por ordenação
    ordering = django_filters.OrderingFilter(
        fields=(
            ('data_competencia', 'data_competencia'),
            ('data_vencimento', 'data_vencimento'),
            ('valor', 'valor'),
            ('descricao', 'descricao'),
            ('categoria__nome', 'categoria'),
        ),
    )

    class Meta:
        model = Pagamento
        fields = ['status', 'categoria'] # Permite filtros exatos por status e ID de categoria