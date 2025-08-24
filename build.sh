#!/usr.bin/env bash
# Esce immediatamente se un comando fallisce
set -o errexit

echo "--- Inizio dello script di build ---"

# 1. Aggiorna l'elenco dei pacchetti con i permessi di amministratore
echo "Aggiornamento dei pacchetti di sistema (apt-get update)..."
sudo apt-get update

# 2. Installa le dipendenze di sistema (Poppler e Tesseract) con sudo
echo "Installazione di Tesseract OCR, del pacchetto lingua italiana e di Poppler..."
sudo apt-get install -y tesseract-ocr tesseract-ocr-ita poppler-utils

# 3. Installa i pacchetti Python come da requirements.txt
echo "Installazione delle dipendenze Python (pip)..."
pip install -r requirements.txt

echo "--- Script di build completato con successo ---"
