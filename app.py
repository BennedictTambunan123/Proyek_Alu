from flask import Flask, render_template, request
import cv2
import numpy as np
import base64
from indentifikasi import identifikasi_warna_dominan_recursive

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            gambar_asli = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

            tinggi, lebar, _ = gambar_asli.shape

            ukuran_subregion = 100
            hasil = identifikasi_warna_dominan_recursive(gambar_asli, ukuran_subregion)

            if hasil != "Tidak Dapat Dikenali":
                _, buffer_main = cv2.imencode('.png', gambar_asli)
                image_base64_main = base64.b64encode(buffer_main).decode('utf-8')

                return render_template('result.html', 
                                       image_base64_main=image_base64_main, 
                                       warna_dominan=hasil)
            else:
                print("Tidak dapat menampilkan gambar")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
