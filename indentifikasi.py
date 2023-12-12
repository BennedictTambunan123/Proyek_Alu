import cv2
import numpy as np
from collections import Counter
import base64

def identifikasi_warna_dominan_subregion(subregion):
    hsv_subregion = cv2.cvtColor(subregion, cv2.COLOR_BGR2HSV)

    warna = {
        "Merah": ([0, 100, 100], [10, 255, 255]),
        "Hijau": ([40, 40, 40], [80, 255, 255]),
        "Biru": ([90, 50, 50], [130, 255, 255]),
        "Kuning": ([20, 100, 100], [40, 255, 255]),
        "Ungu": ([120, 50, 50], [150, 255, 255]),
        "Putih": ([0, 0, 200], [180, 30, 255]),
        "Coklat": ([10, 80, 20], [30, 255, 200]),
        "Coklat Muda": ([20, 80, 40], [40, 255, 200]),
        "Abu-Abu": ([0, 0, 80], [180, 20, 200]),
        "Biru Muda": ([90, 50, 50], [130, 255, 255]),
        "Orange": ([10, 100, 100], [20, 255, 255]),
        "Biru Tua": ([100, 50, 50], [140, 255, 255]),
        "Pink": ([150, 50, 50], [170, 255, 255]),
        "Hijau Tua": ([70, 40, 40], [90, 255, 255]),
        "Hitam": ([0, 0, 0], [180, 255, 30])
    }

    jumlah_piksel_warna = {nama_warna: 0 for nama_warna in warna}

    for nama_warna, (lower, upper) in warna.items():
        mask = cv2.inRange(hsv_subregion, np.array(lower), np.array(upper))
        jumlah_piksel = cv2.countNonZero(mask)
        jumlah_piksel_warna[nama_warna] = jumlah_piksel

    sorted_colors = [warna for warna, _ in Counter(jumlah_piksel_warna).most_common()]

    return sorted_colors[:3]

def identifikasi_warna_dominan_recursive(gambar, ukuran_subregion):
    if gambar.size <= ukuran_subregion:
        return identifikasi_warna_dominan_subregion(gambar)

    tinggi, lebar, _ = gambar.shape

    if tinggi <= ukuran_subregion and lebar <= ukuran_subregion:
        return identifikasi_warna_dominan_subregion(gambar)

    subregions = [
        gambar[:tinggi // 2, :lebar // 2],
        gambar[:tinggi // 2, lebar // 2:],
        gambar[tinggi // 2:, :lebar // 2],
        gambar[tinggi // 2:, lebar // 2:]
    ]   

    hasil_subregions = [identifikasi_warna_dominan_recursive(subregion, ukuran_subregion) for subregion in subregions]

    hasil_subregions = [hasil for hasil in hasil_subregions if hasil != "Tidak Dapat Dikenali"]

    if not hasil_subregions:
        return "Tidak Dapat Dikenali"

    warna_dominan = [warna for sublist in hasil_subregions for warna in sublist]

    warna_dominan = [warna for warna, _ in Counter(warna_dominan).most_common()]

    return warna_dominan