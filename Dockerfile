# Usa un'immagine Python 3.10 ufficiale e leggera come base
FROM python:3.10-slim

# Imposta la cartella di lavoro all'interno del container a /app
WORKDIR /app

# Aggiorna l'elenco dei pacchetti e installa le dipendenze di sistema (Tesseract e Poppler)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ita \
    poppler-utils \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copia il file dei requisiti e installa le dipendenze Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice della tua applicazione
COPY . .

# Esponi la porta 8080 per Fly.io
EXPOSE 8080

# Comando per avviare l'applicazione in produzione con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
