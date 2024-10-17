from flask import Flask, render_template, request, redirect, url_for
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

app = Flask(_name_)

# ÊÍãíá ÇáäãæĞÌ ÇáãÏÑÈ
model = load_model('Usmodel.h5')

# ãÌáÏ áÍİÙ ÇáÕæÑ ÇáãÑİæÚÉ ãÄŞÊğÇ
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ÕİÍÉ ÇáæÇÌåÉ ÇáÑÆíÓíÉ
@app.route('/')
def index():
    return render_template('index.html')

# ãÚÇáÌÉ ÇáÕæÑÉ æÊÔÛíá ÇáäãæĞÌ
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # ÊÍãíá ÇáÕæÑÉ æÊÍÖíÑåÇ ááäãæĞÌ
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # ÊØÈíÚ ÇáÕæÑÉ

        # ÊæŞÚ ÇáäãæĞÌ
        prediction = model.predict(img_array)
        class_index = np.argmax(prediction)
        result = 'ØÈíÚí' if class_index == 0 else 'ÛíÑ ØÈíÚí'

        # ÚÑÖ ÇáäÊíÌÉ ãÚ ÇáÕæÑÉ
        return render_template('index.html', result=result, image_url=url_for('uploaded_file', filename=file.filename))

# áÊŞÏíã ÇáãáİÇÊ ÇáãÑİæÚÉ (ÇáÕæÑ)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if _name_ == '_main_':
    app.run(debug=True)
