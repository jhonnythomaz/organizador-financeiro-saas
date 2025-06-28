# api/serializers.py
from rest_framework import serializers
from .models import Pagamento, Categoria, Cliente, PerfilUsuario

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome_empresa']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'descricao']
        read_only_fields = ('cliente',)

class PagamentoSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True, allow_null=True)
    
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Pagamento
        fields = [
            'id', 'descricao', 'valor', 'data_competencia', 'data_vencimento', 
            'data_pagamento', 'status', 'numero_nota_fiscal', 'categoria_id', 
            'categoria_nome', 'data_criacao'
        ]
        read_only_fields = ('cliente',)

    def validate_categoria_id(self, value):
        cliente_contexto = self.context['request'].user.perfilusuario.cliente
        if value and value.cliente != cliente_contexto:
            raise serializers.ValidationError("Esta categoria não pertence à sua empresa.")
        return value