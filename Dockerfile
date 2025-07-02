# Dockerfile do Backend (na raiz do projeto)

# Estágio 1: Builder de Dependências
FROM python:3.11-slim as builder
WORKDIR /usr/src/app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Estágio 2: Imagem Final de Produção
FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app

# Copia as dependências já instaladas
COPY --from=builder /usr/src/app /usr/src/app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia o código da aplicação
COPY . .
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi:application"]