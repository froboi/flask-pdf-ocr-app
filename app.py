import os
import tempfile
from flask import Flask, request, render_template, send_file, session, redirect, url_for
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

# Creazione dell'istanza dell'app Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chiave segreta per la gestione della sessione

# Configurazione della cartella per gli upload (sebbene useremo file temporanei)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. Controlla se il file è stato inviato
        if 'pdf_file' not in request.files:
            return redirect(request.url)
        
        file = request.files['pdf_file']

        # 2. Controlla se il nome del file è vuoto o non è un PDF
        if file.filename == '' or not file.filename.lower().endswith('.pdf'):
            return redirect(request.url)

        # 3. Gestione sicura dei file con una directory temporanea
        with tempfile.TemporaryDirectory() as temp_dir:
            pdf_path = os.path.join(temp_dir, file.filename)
            file.save(pdf_path)

            try:
                # 4. Conversione del PDF in una lista di immagini (PIL objects)
                # È necessario che 'poppler' sia installato nel sistema
                images = convert_from_path(pdf_path)
                
                full_text = ""
                # 5. Esecuzione dell'OCR su ogni pagina/immagine
                for i, image in enumerate(images):
                    # È necessario che 'tesseract' sia installato nel sistema
                    text = pytesseract.image_to_string(image, lang='ita') # Specifica la lingua italiana
                    full_text += f"--- Pagina {i+1} ---\n"
                    full_text += text + "\n\n"
                
                # 6. Salva il testo estratto nella sessione per il download successivo
                session['extracted_text'] = full_text
                
                # 7. Renderizza la pagina mostrando il testo
                return render_template('index.html', extracted_text=full_text, file_uploaded=True)

            except Exception as e:
                # Gestione di eventuali errori durante la conversione o l'OCR
                error_message = f"Si è verificato un errore: {e}. Assicurati che Poppler e Tesseract OCR siano installati correttamente."
                return render_template('index.html', error=error_message)

    # Per le richieste GET, mostra semplicemente la pagina di upload
    return render_template('index.html', extracted_text=None, file_uploaded=False)


@app.route('/download')
def download_text():
    """
    Crea un file .txt temporaneo con il testo estratto e lo rende scaricabile.
    """
    extracted_text = session.get('extracted_text', 'Nessun testo da scaricare.')

    # Crea un file temporaneo per il testo
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt', encoding='utf-8') as temp_file:
        temp_file.write(extracted_text)
        temp_file_path = temp_file.name
    
    # Invia il file all'utente e poi lo elimina
    return send_file(
        temp_file_path,
        as_attachment=True,
        download_name='testo_estratto.txt',
        mimetype='text/plain'
    )

@app.route('/clear')
def clear_session():
    """
    Pulisce la sessione e reindirizza alla home page.
    """
    session.pop('extracted_text', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
