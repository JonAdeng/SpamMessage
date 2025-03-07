from flask import Flask, request, jsonify
import torch
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Mengizinkan akses dari frontend Vue.js

# Path Model & Tokenizer
MODEL_PATH = "./dataset/indobert_finetuned.pkl"
TOKENIZER_PATH = "./dataset/indobert_tokenizer.pkl"

# Load Tokenizer
def load_tokenizer(tokenizer_path):
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)
    return tokenizer

# Load Model
def load_model(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

# Load model dan tokenizer saat startup
tokenizer = load_tokenizer(TOKENIZER_PATH)
model = load_model(MODEL_PATH)

# Endpoint API
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        user_input = data.get("text", "")

        if not user_input:
            return jsonify({"error": "Teks tidak boleh kosong"}), 400

        # Tokenisasi input
        tokens = tokenizer.encode_plus(user_input, padding=True, truncation=True, return_tensors="pt")

        # Prediksi Model
        with torch.no_grad():
            output = model(**tokens)
            prediction = torch.argmax(output.logits, dim=1).item()

        # Konversi Prediksi ke Label
        label_dict = {
            0: {"label": "Pesan Biasa", "color": "#4CAF50"},
            1: {"label": "Pesan Spam", "color": "#FF5722"},
            2: {"label": "Pesan Promosi", "color": "#FFC107"},
        }
        
        hasil = label_dict.get(prediction, {"label": "Kategori Tidak Diketahui", "color": "#9E9E9E"})

        return jsonify({
            "input_text": user_input,
            "prediction": hasil["label"],
            "color": hasil["color"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)