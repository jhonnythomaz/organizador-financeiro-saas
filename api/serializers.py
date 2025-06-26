# api/serializers.py
from rest_framework import serializers
from .models import Pagamento, Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']


class PagamentoSerializer(serializers.ModelSerializer):
    # Para mostrar o nome da categoria ao invés do ID
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Pagamento
        fields = [
            'id',
            'descricao',
            'valor',
            'data_vencimento',
            'data_pagamento',
            'categoria', # Usado para criar/atualizar
            'categoria_nome', # Usado para exibir
            'status',
            'data_criacao'
        ]
        # O usuário será pego automaticamente do request, não precisa estar no JSON
        read_only_fields = ('usuario',)