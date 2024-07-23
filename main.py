from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import numpy as np
import os
from collections import Counter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def create_upload_folder():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

def get_top_colors(image_path, num_colors=10):
    image = Image.open(image_path)
    image = image.convert('RGB')
    image_np = np.array(image)
    pixels = image_np.reshape(-1, 3)
    pixel_counts = Counter(map(tuple, pixels))
    top_colors = pixel_counts.most_common(num_colors)
    return [(f'#{r:02x}{g:02x}{b:02x}', (r, g, b)) for (r, g, b), count in top_colors]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            top_colors = get_top_colors(file_path)
            return render_template('index.html', top_colors=top_colors)
    return render_template('index.html')

if __name__ == '__main__':
    create_upload_folder()
    app.run(debug=True)