# Usa uma imagem oficial do Python
FROM python:3.9

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta 8080 para comunicação externa
EXPOSE 8080

# Comando para rodar a API (AJUSTADO PARA O SEU ARQUIVO .py)
CMD ["python", "facebook_ads_connector.py"]
