#!/usr/bin/env bash
# Esce immediatamente se un comando fallisce, per evitare errori nascosti.
set -o errexit

echo "--- Inizio script di build ---"

# Passo 1: Aggiorna l'elenco dei pacchetti e installa le dipendenze di sistema.
# Usiamo '&&' per assicurarci che l'installazione parta solo se l'update ha successo.
echo "Fase 1: Aggiornamento dei pacchetti di sistema e installazione di Tesseract e Poppler..."
sudo apt-get update && sudo apt-get install -y tesseract-ocr tesseract-ocr-ita poppler-utils

# Passo 2: Installa le dipendenze Python dal file requirements.txt.
echo "Fase 2: Installazione delle dipendenze Python..."
pip install -r requirements.txt

echo "--- Script di build completato con successo. Avvio dell'applicazione... ---"
