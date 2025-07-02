# api/serializers.py
from rest_framework import serializers
from .models import Pagamento, Categoria, Cliente, PerfilUsuario, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

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
    usuario = UserSerializer(read_only=True)
    
    # --- CORREÇÃO: Novo campo para o status calculado ---
    status_display = serializers.CharField(source='status_calculado', read_only=True)
    
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Pagamento
        fields = [
            'id', 'descricao', 'valor', 'data_competencia', 'data_vencimento', 
            'data_pagamento', 'status', 'status_display', 'numero_nota_fiscal', 
            'categoria_id', 'categoria_nome', 'usuario', 'data_criacao'
        ]
        read_only_fields = ('id', 'usuario', 'data_criacao', 'categoria_nome', 'status_display')

    def validate_categoria_id(self, value):
        cliente_contexto = self.context['request'].user.perfilusuario.cliente
        if value and value.cliente != cliente_contexto:
            raise serializers.ValidationError("Esta categoria não pertence à sua empresa.")
        return value