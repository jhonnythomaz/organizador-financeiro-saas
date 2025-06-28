# setup_tenant.py
import os
import django

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Agora podemos importar os modelos
from django.contrib.auth.models import User
from api.models import Cliente, PerfilUsuario

def run():
    # --- Limpeza (Opcional, mas bom para rodar várias vezes) ---
    # User.objects.filter(is_superuser=True).delete()
    # Cliente.objects.all().delete()
    # print("Dados antigos de teste limpos.")

    # --- Defina aqui os dados do seu primeiro usuário/cliente ---
    USERNAME = 'jhonny_admin'
    PASSWORD = '123' # Troque por uma senha real
    EMAIL = 'jhonny@exemplo.com'
    NOME_EMPRESA = 'Alecrim Cuidados Especiais'

    # --- Lógica de Criação ---
    if not User.objects.filter(username=USERNAME).exists():
        print(f"Criando superusuário: {USERNAME}")
        super_usuario = User.objects.create_superuser(
            username=USERNAME,
            email=EMAIL,
            password=PASSWORD
        )

        print(f"Criando cliente: {NOME_EMPRESA}")
        cliente = Cliente.objects.create(nome_empresa=NOME_EMPRESA)

        print(f"Associando usuário '{USERNAME}' ao cliente '{NOME_EMPRESA}'...")
        PerfilUsuario.objects.create(usuario=super_usuario, cliente=cliente)

        print("\nSetup concluído com sucesso!")
    else:
        print(f"Usuário '{USERNAME}' já existe. Nenhum dado novo foi criado.")

# Roda a função principal
if __name__ == '__main__':
    run()