import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. DEFINISI FUNGSI KEANGGOTAAN TRAPESIUM UNTUK VARIABEL USIA
# ==========================================================

def mf_bayi(x):
    """Bayi / Anak Usia Dini: (a=0, b=0, c=3, d=5)"""
    kondisi = [
        (x >= 0.0) & (x <= 3.0),
        (x > 3.0) & (x < 5.0),
        (x <= 0.0) | (x >= 5.0)
    ]
    pilihan = [
        1.0,
        (5.0 - x) / 2.0,
        0.0
    ]
    return np.select(kondisi, pilihan)


def mf_anak(x):
    """Anak-anak: (a=4, b=6, c=9, d=11)"""
    kondisi = [
        (x <= 4.0) | (x >= 11.0),
        (x > 4.0) & (x < 6.0),
        (x >= 6.0) & (x <= 9.0),
        (x > 9.0) & (x < 11.0)
    ]
    pilihan = [
        0.0,
        (x - 4.0) / 2.0,
        1.0,
        (11.0 - x) / 2.0
    ]
    return np.select(kondisi, pilihan)


def mf_remaja(x):
    """Remaja: (a=10, b=12, c=17, d=19)"""
    kondisi = [
        (x <= 10.0) | (x >= 19.0),
        (x > 10.0) & (x < 12.0),
        (x >= 12.0) & (x <= 17.0),
        (x > 17.0) & (x < 19.0)
    ]
    pilihan = [
        0.0,
        (x - 10.0) / 2.0,
        1.0,
        (19.0 - x) / 2.0
    ]
    return np.select(kondisi, pilihan)


def mf_pemuda(x):
    """Pemuda: (a=15, b=17, c=22, d=24)"""
    kondisi = [
        (x <= 15.0) | (x >= 24.0),
        (x > 15.0) & (x < 17.0),
        (x >= 17.0) & (x <= 22.0),
        (x > 22.0) & (x < 24.0)
    ]
    pilihan = [
        0.0,
        (x - 15.0) / 2.0,
        1.0,
        (24.0 - x) / 2.0
    ]
    return np.select(kondisi, pilihan)


def mf_dewasa(x):
    """Dewasa: (a=20, b=25, c=60, d=65)"""
    kondisi = [
        (x <= 20.0) | (x >= 65.0),
        (x > 20.0) & (x < 25.0),
        (x >= 25.0) & (x <= 60.0),
        (x > 60.0) & (x < 65.0)
    ]
    pilihan = [
        0.0,
        (x - 20.0) / 5.0,
        1.0,
        (65.0 - x) / 5.0
    ]
    return np.select(kondisi, pilihan)


def mf_lansia(x):
    """Lanjut Usia (Lansia): (a=60, b=65, c=80, d=80)"""
    kondisi = [
        x <= 60.0,
        (x > 60.0) & (x < 65.0),
        x >= 65.0
    ]
    pilihan = [
        0.0,
        (x - 60.0) / 5.0,
        1.0
    ]
    return np.select(kondisi, pilihan)


# ==========================================================
# 2. GENERATE DOMAIN SEMESTA PEMBICARAAN (0 - 80 Tahun)
# ==========================================================
x_semesta = np.linspace(0.0, 80.0, 1000)

y_bayi = mf_bayi(x_semesta)
y_anak = mf_anak(x_semesta)
y_remaja = mf_remaja(x_semesta)
y_pemuda = mf_pemuda(x_semesta)
y_dewasa = mf_dewasa(x_semesta)
y_lansia = mf_lansia(x_semesta)


# ==========================================================
# 3. VISUALISASI GRAFIK FUNGSI KEANGGOTAAN USIA
# ==========================================================
plt.figure(figsize=(12, 6))

plt.plot(x_semesta, y_bayi, label='Bayi / Anak Usia Dini', color='#1f77b4', linewidth=2)
plt.plot(x_semesta, y_anak, label='Anak-anak', color='#ff7f0e', linewidth=2)
plt.plot(x_semesta, y_remaja, label='Remaja', color='#2ca02c', linewidth=2)
plt.plot(x_semesta, y_pemuda, label='Pemuda', color='#d62728', linewidth=2)
plt.plot(x_semesta, y_dewasa, label='Dewasa', color='#9467bd', linewidth=2)
plt.plot(x_semesta, y_lansia, label='Lanjut Usia (Lansia)', color='#8c564b', linewidth=2)

plt.title('Grafik Fungsi Keanggotaan Trapesium Variabel Usia', fontsize=14, fontweight='bold')
plt.xlabel('Usia (Tahun)', fontsize=11)
plt.ylabel('Derajat Keanggotaan μ(x)', fontsize=11)
plt.xlim(0, 80)
plt.ylim(-0.05, 1.1)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='center right', fontsize=9)
plt.tight_layout()

