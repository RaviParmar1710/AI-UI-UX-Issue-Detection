from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from PIL import Image
import numpy as np
import tensorflow as tf

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE_MB = 5  # Optional: max file size limit

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB limit

model = tf.keras.models.load_model('model/ui_ux_model.keras')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_image(path):
    img = Image.open(path).resize((224, 224))
    img = np.expand_dims(np.array(img) / 255.0, axis=0)
    pred = model.predict(img)[0][0]
    return "Good UX" if pred < 0.5 else "Bad UX", round(float(pred), 1)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "screenshot" not in request.files:
            flash("❌ No file part in request.")
            return redirect(request.url)
        
        file = request.files["screenshot"]

        if file.filename == "":
            flash("❌ No file selected.")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("⚠️ Invalid file type. Please upload a JPG or PNG image.")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            label, confidence = predict_image(filepath)
            return render_template("result.html", img_path=filepath, label=label, confidence=confidence)
        except Exception as e:
            flash("🚫 Error processing image. Please try again.")
            print(f"Prediction error: {e}")
            return redirect(request.url)

    return render_template("index.html")

@app.errorhandler(413)
def request_entity_too_large(error):
    return "⚠️ File too large. Please upload an image smaller than 1 MB.", 413


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)






#     python app.py


