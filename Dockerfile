# Usa a imagem oficial do Python 3.11 (leve)
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Define variáveis de ambiente para otimizar o Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copia apenas o arquivo de dependências primeiro (aproveita o cache do Docker)
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação para dentro do container
COPY . .

# Expõe a porta que o FastAPI vai rodar
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]