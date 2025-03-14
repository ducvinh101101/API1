from flask import Flask, request, jsonify
import numpy as np
import io
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Mở CORS để frontend có thể truy cập

# Load mô hình
model = load_model("last.h5")

# Danh sách nhãn lớp
class_labels = ['glioma', 'meningioma', 'notumor', 'pituitary']

def preprocess_image(image):
    """Tiền xử lý ảnh để đưa vào model"""
    image = image.convert("RGB")
    image = image.resize((128, 128))
    image = np.array(image, dtype=np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict', methods=['POST'])
def predict():
    """Nhận ảnh từ request, dự đoán bằng mô hình, và trả về kết quả"""
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    processed_img = preprocess_image(image)

    # Dự đoán
    prediction = model.predict(processed_img)
    predicted_class = np.argmax(prediction)
    confidence = float(np.max(prediction))

    result = {
        "diagnosis": class_labels[predicted_class],
        "confidence": confidence
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
