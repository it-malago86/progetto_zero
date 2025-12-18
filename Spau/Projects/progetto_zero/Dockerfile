# Usa un'immagine Python ufficiale leggera
FROM python:3.11-slim

# Imposta la cartella di lavoro nel contenitore
WORKDIR /app

# Installa le dipendenze necessarie
RUN pip install --no-cache-dir fastapi uvicorn aiofiles sqlalchemy psycopg2-binary

# Copia il tuo codice dentro il contenitore
COPY main.py .

# Apri la porta 8000
EXPOSE 8000

# Avvia il server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
