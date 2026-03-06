FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema se necessário
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do projeto
COPY . .

# Expor a porta que o FastAPI usará
EXPOSE 8000

# Comando para rodar a aplicação
# Usamos o uvicorn apontando para o app dentro de web.main
CMD ["uvicorn", "web.main:app", "--host", "0.0.0.0", "--port", "8000"]
