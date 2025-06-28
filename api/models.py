# api/models.py
from django.db import models
from django.contrib.auth.models import User

# --- Modelo do Inquilino (Tenant) ---
class Cliente(models.Model):
    nome_empresa = models.CharField(max_length=200, unique=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_empresa

# --- Modelo para estender o User e ligá-lo a um Cliente ---
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario.username} -> {self.cliente.nome_empresa}"

# --- Modelos de Dados, agora ligados ao Cliente ---
class Categoria(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.cliente.nome_empresa})"

STATUS_CHOICES = [
    ('Pendente', 'Pendente'),
    ('Pago', 'Pago'),
    ('Atrasado', 'Atrasado'),
]

class Pagamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagamentos')
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_competencia = models.DateField()
    data_vencimento = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pendente')
    numero_nota_fiscal = models.CharField(max_length=50, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao