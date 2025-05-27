from flask import Flask, request, send_file, jsonify, render_template
from rembg import remove
from PIL import Image
from flask_cors import CORS
import io
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_folder = os.path.join(project_root, 'templates')
static_folder = os.path.join(project_root, 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "Tidak ada file gambar"}), 400

    file = request.files["image"]

    # Validasi ekstensi
    ekstensi_valid = [".jpg", ".jpeg", ".png", ".webp"]
    filename = file.filename
    if not filename:
        return jsonify({"error": "Nama file tidak valid"}), 400

    _, ekst = os.path.splitext(filename.lower())
    if ekst not in ekstensi_valid:
        return jsonify({"error": f"Format {ekst} tidak didukung."}), 400

    try:
        # Buka file sebagai PIL Image
        input_image = Image.open(file.stream)

        # Proses hapus background
        output_image = remove(input_image)

        # Simpan hasil ke memory (bukan file)
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        # Kirim hasil sebagai file gambar
        return send_file(output_buffer, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": f"Gagal memproses gambar: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
