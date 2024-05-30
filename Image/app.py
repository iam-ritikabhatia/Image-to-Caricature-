from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CARICATURE_FOLDER = 'caricatures'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CARICATURE_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    if file:
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Process the image to create a caricature
            caricature_path = generate_caricature(filepath)

            if caricature_path:
                return jsonify({'success': True, 'caricatureUrl': caricature_path})
            else:
                return jsonify({'success': False, 'error': 'Failed to generate caricature'})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

def generate_caricature(filepath):
    try:
        img = Image.open(filepath)
        
        # Convert image to RGB mode if it's in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        caricature = ImageOps.posterize(img, 2)  # Simplified example of a caricature effect
        caricature_filename = os.path.basename(filepath)
        caricature_path = os.path.join(CARICATURE_FOLDER, caricature_filename)
        caricature.save(caricature_path)
        return f'/caricatures/{caricature_filename}'
    except Exception as e:
        print(f"Error generating caricature: {e}")
        return None



@app.route('/caricatures/<filename>')
def caricature(filename):
    return send_from_directory(CARICATURE_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
