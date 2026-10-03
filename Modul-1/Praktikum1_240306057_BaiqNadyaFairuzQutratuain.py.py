import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. DEFINISI FUNGSI CRISP DAN FUZZY
# ==========================================================
def crisp_kritis(waktu, threshold=8.0):
    """
    Fungsi karakteristik crisp.
    Mengembalikan 1.0 jika waktu >= threshold, selain itu 0.0.
    """
    waktu = np.asarray(waktu, dtype=float)
    return np.where(waktu >= threshold, 1.0, 0.0)

def fuzzy_kritis(waktu, a=4.0, b=12.0):
    """
    Fungsi keanggotaan fuzzy linear naik.
    - x < a       : derajat 0
    - a <= x <= b : derajat (x - a) / (b - a)
    - x > b       : derajat 1
    """
    waktu = np.asarray(waktu, dtype=float)
    derajat = (waktu - a) / (b - a)
    return np.clip(derajat, 0.0, 1.0)

# ==========================================================
# 2. PENGUJIANKU DATA UJI (SOAL NO. 3)
# ==========================================================
data_uji = [2, 4, 6, 7.9, 8.0, 8.1, 10, 12, 16, 24]

print("=" * 68)
print(f"{'Waktu (Jam)':<12} | {'Crisp':<8} | {'Fuzzy mu(x)':<12} | {'Interpretasi Fuzzy'}")
print("=" * 68)

for w in data_uji:
    c_val = float(crisp_kritis(w))
    f_val = float(fuzzy_kritis(w))
    interpretasi = f"Tingkat Kritis {f_val * 100:.1f}%"
    print(f"{w:<12.1f} | {c_val:<8.1f} | {f_val:<12.3f} | {interpretasi}")

print("=" * 68)

# ==========================================================
# 3. VISUALISASI GRAFIK KOMPARASI (SOAL NO. 4)
# ==========================================================
# Semesta pembicaraan 0 <= x <= 24 jam
x_domain = np.linspace(0, 24, 1000)

y_crisp = crisp_kritis(x_domain)
y_fuzzy = fuzzy_kritis(x_domain)

plt.figure(figsize=(10, 5))

# Plot Logika Crisp
plt.step(x_domain, y_crisp, label='Crisp (Threshold >= 8 jam)', 
         color='#d9534f', linewidth=2.5, where='post')

# Plot Logika Fuzzy
plt.plot(x_domain, y_fuzzy, label='Fuzzy Linear Naik [4, 12] jam', 
         color='#0275d8', linewidth=2.5)

# Penanda titik batas kritis (7.9 jam vs 8.0 jam)
plt.axvline(x=7.9, color='gray', linestyle='--', alpha=0.6)
plt.axvline(x=8.0, color='gray', linestyle='--', alpha=0.6)

plt.title('Sistem Prioritas Tiket Helpdesk TI: Kategori "Kritis / Eskalasi Cepat"', fontsize=12, fontweight='bold')
plt.xlabel('Waktu Tunggu Penyelesaian Tiket (Jam)', fontsize=11)
plt.ylabel('Derajat Keanggotaan / Nilai Kebenaran', fontsize=11)
plt.xlim(0, 24)
plt.ylim(-0.05, 1.1)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()

# Simpan grafik
plt.savefig('grafik_prioritas_tiket_helpdesk.png', dpi=300)
plt.show()



