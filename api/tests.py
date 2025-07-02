# api/tests.py

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Cliente, PerfilUsuario, Categoria, Pagamento

@pytest.mark.django_db
def test_categoria_access_control():
    # --- 1. Preparação (Arrange) ---
    cliente_a = Cliente.objects.create(nome_empresa='Empresa A')
    user_a = User.objects.create_user(username='usera', password='password123')
    PerfilUsuario.objects.create(usuario=user_a, cliente=cliente_a)
    
    cliente_b = Cliente.objects.create(nome_empresa='Empresa B')
    user_b = User.objects.create_user(username='userb', password='password123')
    PerfilUsuario.objects.create(usuario=user_b, cliente=cliente_b)

    Categoria.objects.create(cliente=cliente_a, nome='Categoria de A')

    client = APIClient()

    # --- 2. Ação e Verificação (Act & Assert) ---

    # Teste 1: Um usuário não logado NÃO PODE ver as categorias.
    response_anonimo = client.get('/api/categorias/')
    assert response_anonimo.status_code == 401

    # Teste 2: Usuário A faz login via JWT e tenta ver suas categorias.
    token_response_a = client.post('/api/token/', {'username': 'usera', 'password': 'password123'})
    assert token_response_a.status_code == 200
    access_token_a = token_response_a.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token_a}')
    response_a = client.get('/api/categorias/')
    assert response_a.status_code == 200
    assert len(response_a.data) == 1
    assert response_a.data[0]['nome'] == 'Categoria de A'

    # Teste 3: Usuário B faz login via JWT e tenta ver as categorias.
    token_response_b = client.post('/api/token/', {'username': 'userb', 'password': 'password123'})
    assert token_response_b.status_code == 200
    access_token_b = token_response_b.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token_b}')
    response_b = client.get('/api/categorias/')
    assert response_b.status_code == 200
    assert len(response_b.data) == 0

    print("Teste de isolamento de dados de Categoria passou com sucesso!")

# Adicione esta nova função em api/tests.py

# A anotação @pytest.fixture cria uma "função de setup" que podemos reutilizar em vários testes.
# Isso evita repetir a criação de usuários e clientes.
@pytest.fixture
def setup_clientes_e_usuarios():
    # Cliente A
    cliente_a = Cliente.objects.create(nome_empresa='Empresa A')
    user_a = User.objects.create_user(username='usera', password='password123')
    PerfilUsuario.objects.create(usuario=user_a, cliente=cliente_a)

    # Cliente B
    cliente_b = Cliente.objects.create(nome_empresa='Empresa B')
    user_b = User.objects.create_user(username='userb', password='password123')
    PerfilUsuario.objects.create(usuario=user_b, cliente=cliente_b)

    return {'cliente_a': cliente_a, 'user_a': user_a, 'cliente_b': cliente_b, 'user_b': user_b}

@pytest.mark.django_db
def test_pagamentos_filtros_e_ordenacao(setup_clientes_e_usuarios):
    # --- 1. Preparação (Arrange) ---
    cliente_a = setup_clientes_e_usuarios['cliente_a']
    
    # Criando categorias para o Cliente A
    cat_moradia = Categoria.objects.create(cliente=cliente_a, nome='Moradia')
    cat_transporte = Categoria.objects.create(cliente=cliente_a, nome='Transporte')

    # Criando pagamentos para o Cliente A
    Pagamento.objects.create(cliente=cliente_a, descricao='Aluguel', valor=1500, data_competencia='2024-07-01', data_vencimento='2024-07-05', status='Pago', categoria=cat_moradia)
    Pagamento.objects.create(cliente=cliente_a, descricao='Gasolina', valor=200, data_competencia='2024-07-10', data_vencimento='2024-07-10', status='Pago', categoria=cat_transporte)
    Pagamento.objects.create(cliente=cliente_a, descricao='Conta de Luz', valor=300, data_competencia='2024-06-25', data_vencimento='2024-07-10', status='Pendente')
    
    client = APIClient()

    # Login como Usuário A
    token_response = client.post('/api/token/', {'username': 'usera', 'password': 'password123'})
    access_token = token_response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # --- 2. Ação e Verificação (Act & Assert) ---

    # Teste 1: Listagem sem filtros (deve retornar 3 pagamentos)
    response = client.get('/api/pagamentos/')
    assert response.status_code == 200
    assert len(response.data) == 3

    # Teste 2: Filtrando por status "Pago" (deve retornar 2 pagamentos)
    response = client.get('/api/pagamentos/?status=Pago')
    assert response.status_code == 200
    assert len(response.data) == 2
    # Verifica se todos os itens retornados têm o status correto
    assert all(item['status'] == 'Pago' for item in response.data)

    # Teste 3: Filtrando por categoria "Moradia" (deve retornar 1 pagamento)
    response = client.get(f'/api/pagamentos/?categoria={cat_moradia.id}')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['descricao'] == 'Aluguel'

    # Teste 4: Filtrando por descrição "luz" (deve retornar 1 pagamento)
    response = client.get('/api/pagamentos/?descricao=luz')
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['descricao'] == 'Conta de Luz'

    # Teste 5: Ordenando por valor ascendente (o primeiro deve ser Gasolina)
    response = client.get('/api/pagamentos/?ordering=valor')
    assert response.status_code == 200
    assert response.data[0]['descricao'] == 'Gasolina' # Gasolina (200) < Luz (300) < Aluguel (1500)

    # Teste 6: Ordenando por valor descendente (o primeiro deve ser Aluguel)
    response = client.get('/api/pagamentos/?ordering=-valor')
    assert response.status_code == 200
    assert response.data[0]['descricao'] == 'Aluguel'

    print("Teste de filtros e ordenação de Pagamentos passou com sucesso!")