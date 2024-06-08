from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

from keras._tf_keras.keras.preprocessing.image import load_img
from keras._tf_keras.keras.preprocessing.image import img_to_array
from keras._tf_keras.keras.applications.vgg16 import preprocess_input
from keras._tf_keras.keras.applications.vgg16 import decode_predictions
from keras._tf_keras.keras.applications.resnet50 import ResNet50


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/result',methods=['POST'])
def result():
     if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            model = ResNet50()
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = "./uploads/"+filename
            image = load_img(image_path, target_size=(224, 224))
            image = img_to_array(image)
            image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
            image = preprocess_input(image)
            yhat = model.predict(image)
            label = decode_predictions(yhat)
            label = label[0][0]
            classification = '%s (%.2f%%)' % (label[1], label[2]*100)
            return render_template('result.html',prediction=classification)

@app.route('/', methods=['GET', 'POST'])
def Home():
 return render_template('upload.html')
    
if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
