#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Installa i pacchetti Python
pip install -r requirements.txt

# 2. Installa le dipendenze di sistema (Poppler e Tesseract)
#    usando il gestore di pacchetti 'apt-get' del sistema operativo di Render
apt-get update
apt-get install -y tesseract-ocr tesseract-ocr-ita poppler-utils
