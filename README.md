# Organizador Financeiro Alecrim

![Dashboard Screenshot](link_para_uma_imagem_do_seu_dashboard.png) <!-- Tire um print da sua tela e adicione aqui -->

Este é um sistema completo de organização financeira construído com Django e React, projetado com uma arquitetura multi-tenant para gerenciar múltiplos clientes.

---

## 🚀 Features

-   **Backend Robusto:** API RESTful construída com Django e Django REST Framework.
-   **Frontend Moderno:** Interface reativa com React, TypeScript e Material-UI.
-   **Autenticação Segura:** Sistema de login com Tokens JWT (Access & Refresh).
-   **Arquitetura Multi-Tenant:** Isolamento total de dados por cliente.
-   **CRUD Completo:** Gerenciamento total de Pagamentos e Categorias.
-   **Dashboard Analítico:** Visualização de gastos por categoria com gráficos interativos.
-   **Relatórios em PDF:** Geração de relatórios financeiros por período.
-   **Painel de Admin:** Superusuários podem gerenciar todos os clientes e "personificar" suas contas.
-   **Busca e Filtros:** Ferramentas poderosas para encontrar informações rapidamente.

---

## 🛠️ Tecnologias Utilizadas

**Backend:**
-   Python 3.11+
-   Django
-   Django REST Framework
-   Simple JWT (para autenticação)
-   PostgreSQL (Banco de Dados)
-   ReportLab (para PDFs)

**Frontend:**
-   Node.js 18+
-   React
-   TypeScript
-   Material-UI (Componentes de UI)
-   Chart.js & react-chartjs-2 (Gráficos)
-   Axios (Requisições HTTP)

---

## ⚙️ Configuração e Instalação

Siga os passos abaixo para rodar o projeto localmente.

### **1. Pré-requisitos**

-   Python 3.11 ou superior
-   Node.js e npm
-   PostgreSQL instalado e rodando

### **2. Configuração do Backend**

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No Mac/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências do Python:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Vamos criar o arquivo `requirements.txt` no próximo passo)*

4.  **Configure o Banco de Dados:**
    -   No PostgreSQL, crie um novo banco de dados chamado `organizador_db`.
    -   Renomeie o arquivo `.env.example` (que vamos criar) para `.env`.
    -   Preencha as variáveis de ambiente no `.env`, incluindo a senha do seu banco.

5.  **Aplique as migrações e crie o primeiro Tenant:**
    ```bash
    python manage.py migrate
    python setup_tenant.py # Isso criará o superusuário e o primeiro cliente
    ```

### **3. Configuração do Frontend**

1.  **Navegue para a pasta do frontend:**
    ```bash
    cd frontend
    ```

2.  **Instale as dependências do Node.js:**
    ```bash
    npm install
    ```

### **4. Rodando a Aplicação**

Você precisará de dois terminais abertos.

-   **Terminal 1 (Backend):**
    ```bash
    # Na pasta raiz do projeto
    python manage.py runserver
    ```

-   **Terminal 2 (Frontend):**
    ```bash
    # Na pasta /frontend
    npm start
    ```

Acesse `http://localhost:3000` no seu navegador. Use as credenciais definidas no script `setup_tenant.py` para fazer login.

---