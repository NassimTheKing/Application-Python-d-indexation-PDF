import os
import re
from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def search_pdf(pdf_path, keyword):
    """Recherche le mot-clé et retourne les phrases exactes"""
    results = []
    reader = PdfReader(pdf_path)
    
    for page_num in range(len(reader.pages)):
        text = reader.pages[page_num].extract_text() or ""
        
        # Trouver toutes les phrases contenant le mot-clé
        sentences = re.split(r'(?<=[.!?])\s+', text)  # Split en phrases
        for sentence in sentences:
            if keyword.lower() in sentence.lower():
                # Nettoyer les espaces multiples
                clean_sentence = ' '.join(sentence.split())
                results.append({
                    'page': page_num + 1,
                    'text': clean_sentence
                })
    
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            keyword = request.form.get('keyword', '').strip()
            
            if keyword:
                results = search_pdf(filepath, keyword)
                return render_template('index.html', 
                                    results=results,
                                    keyword=keyword,
                                    filename=filename)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

