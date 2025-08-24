from flask import Flask, render_template, request
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

app = Flask(__name__)

# --- INIZIO MODIFICA ---
# Specifica il percorso dell'eseguibile di Tesseract per l'ambiente di produzione (Render)
# Questa riga dice a pytesseract dove trovare il programma Tesseract che abbiamo installato.
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
# --- FINE MODIFICA ---

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def ocr_from_pdf(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        full_text = ""
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='ita')
            full_text += f"--- Pagina {i+1} ---\n{text}\n\n"
        return full_text
    except Exception as e:
        # Aggiungiamo un messaggio di errore più specifico per il debug
        error_message = f"Si è verificato un errore: {e}. Assicurati che Poppler e Tesseract OCR siano installati correttamente."
        print(error_message) # Stampa l'errore nel log di Render per il debug
        return error_message

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='Nessun file selezionato')
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error='Nessun file selezionato')

        if file and file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            
            extracted_text = ocr_from_pdf(filepath)
            
            # Pulisce il file dopo l'elaborazione
            os.remove(filepath)
            
            return render_template('index.html', extracted_text=extracted_text, filename=file.filename)
        else:
            return render_template('index.html', error='Formato file non valido. Si prega di caricare un PDF.')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
