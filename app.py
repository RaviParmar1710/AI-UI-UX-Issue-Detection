from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np
import tensorflow as tf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Lazy-load the model
model = None

def load_model():
    global model
    if model is None:
        model = tf.keras.models.load_model('model/ui_ux_model.keras')
    return model

def predict_image(path):
    img = Image.open(path).resize((224, 224))
    img = np.expand_dims(np.array(img) / 255.0, axis=0)
    model = load_model()
    pred = model.predict(img)[0][0]
    return "Good UX" if pred < 0.5 else "Bad UX", round(float(pred), 1)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["screenshot"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        label, confidence = predict_image(filepath)
        return render_template("result.html", img_path=filepath, label=label, confidence=confidence)
    return render_template("index.html")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
