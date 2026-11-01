import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ==========================================================
# 1. FUNGSI KEANGGOTAAN
# ==========================================================
def trapesium(x, a, b, c, d):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    if b > a:
        m = (x > a) & (x < b)
        y[m] = (x[m] - a) / (b - a)
    y[(x >= b) & (x <= c)] = 1.0
    if d > c:
        m = (x > c) & (x < d)
        y[m] = (d - x[m]) / (d - c)
    return y


def segitiga(x, a, b, c):
    x = np.asarray(x, dtype=float)
    y = np.zeros_like(x)
    m = (x > a) & (x <= b)
    y[m] = (x[m] - a) / (b - a)
    m = (x > b) & (x < c)
    y[m] = (c - x[m]) / (c - b)
    return y


# Semesta dan himpunan output (sesuai asesmen)
z = np.linspace(0, 100, 1001)
mf_buruk = trapesium(z, 0, 0, 20, 40)
mf_cukup = segitiga(z, 20, 40, 60)
mf_baik = segitiga(z, 40, 60, 80)
mf_sangat_baik = trapesium(z, 60, 80, 100, 100)
MF_OUTPUT = {"Buruk": mf_buruk, "Cukup": mf_cukup, "Baik": mf_baik, "Sangat Baik": mf_sangat_baik}


# ==========================================================
# 2. IMPLIKASI (MIN) DAN AGREGASI (MAX)
# ==========================================================
def agregasi_mamdani(alpha_per_label):
    """alpha_per_label: {'Buruk': 0.25, 'Cukup': 0.75, ...}"""
    agg = np.zeros_like(z)
    for label, alpha in alpha_per_label.items():
        agg = np.fmax(agg, np.fmin(alpha, MF_OUTPUT[label]))
    return agg


# ==========================================================
# 3. LIMA METODE DEFUZZIFIKASI
# ==========================================================
def daerah_maksimum(agg):
    mu_max = agg.max()
    return z[np.isclose(agg, mu_max)]


def defuzz(agg, metode):
    if agg.sum() == 0:
        return 0.0
    if metode == "centroid":
        return float(np.sum(z * agg) / np.sum(agg))
    if metode == "bisector":
        luas_kumulatif = np.cumsum(agg)
        return float(z[np.searchsorted(luas_kumulatif, luas_kumulatif[-1] / 2.0)])
    titik_max = daerah_maksimum(agg)
    if metode == "mom":
        return float(titik_max.mean())
    if metode == "som":
        return float(titik_max.min())
    if metode == "lom":
        return float(titik_max.max())
    raise ValueError("Metode tidak dikenal")


METODE = ["centroid", "bisector", "mom", "som", "lom"]


def alpha_per_label_dari_aturan(alphas_aturan):
    """Gabungkan alpha aturan yang konsekuennya sama dengan MAX."""
    konsekuen = ["Buruk", "Cukup", "Cukup", "Cukup", "Baik", "Baik", "Cukup", "Baik", "Sangat Baik"]
    hasil = {}
    for alpha, label in zip(alphas_aturan, konsekuen):
        if alpha > 0:
            hasil[label] = max(hasil.get(label, 0.0), alpha)
    return hasil


# ==========================================================
# 4. FUZZIFIKASI DAN ALPHA (dari Praktikum 6)
# ==========================================================
def mf_input(x):
    return {"Rendah": float(trapesium(x, 0, 0, 30, 50)),
            "Sedang": float(segitiga(x, 30, 50, 70)),
            "Tinggi": float(trapesium(x, 50, 70, 100, 100))}


def hitung_alpha_aturan(p, d):
    fp, fd = mf_input(p), mf_input(d)
    urutan = [("Rendah", "Rendah"), ("Rendah", "Sedang"), ("Rendah", "Tinggi"),
              ("Sedang", "Rendah"), ("Sedang", "Sedang"), ("Sedang", "Tinggi"),
              ("Tinggi", "Rendah"), ("Tinggi", "Sedang"), ("Tinggi", "Tinggi")]
    return [min(fp[a], fd[b]) for a, b in urutan]


# ==========================================================
# 5. VISUALISASI PERBANDINGAN
# ==========================================================
def gambar_komparasi(agg, hasil, judul, nama_file):
    warna = {"centroid": "red", "bisector": "purple", "mom": "black", "som": "green", "lom": "orange"}
    plt.figure(figsize=(11, 6))
    plt.plot(z, agg, "b", linewidth=2.5, label="Kurva agregasi")
    plt.fill_between(z, 0, agg, color="skyblue", alpha=0.4)
    for m, v in hasil.items():
        plt.axvline(v, color=warna[m], linestyle="--", linewidth=2, label=f"{m.upper()} ({v:.2f})")
    plt.title(judul, fontweight="bold")
    plt.xlabel("Kinerja Karyawan")
    plt.ylabel("Derajat keanggotaan")
    plt.ylim(-0.05, 1.05)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(nama_file, dpi=200)
    plt.close()


if __name__ == "__main__":
    # --- Contoh: Ahmad Fauzi (Produktivitas 60, Kedisiplinan 65)
    alpha_ahmad = alpha_per_label_dari_aturan(hitung_alpha_aturan(60, 65))
    agg_ahmad = agregasi_mamdani(alpha_ahmad)
    hasil_ahmad = {m: defuzz(agg_ahmad, m) for m in METODE}
    print("CONTOH AHMAD, alpha per label:", alpha_ahmad)
    for m, v in hasil_ahmad.items():
        print(f"  {m.upper():<9}: {v:.2f}")
    gambar_komparasi(agg_ahmad, hasil_ahmad,
                     "Perbandingan 5 Metode Defuzzifikasi (Ahmad Fauzi)", "hasil/p8_komparasi_ahmad.png")

    # --- Tugas 8: Sari Dewi (3 himpunan output aktif)
    alpha_sari = alpha_per_label_dari_aturan(hitung_alpha_aturan(45, 35))
    agg_sari = agregasi_mamdani(alpha_sari)
    hasil_sari = {m: defuzz(agg_sari, m) for m in METODE}
    print("\nTUGAS 8, Sari Dewi, alpha per label:", alpha_sari)
    for m, v in hasil_sari.items():
        print(f"  {m.upper():<9}: {v:.2f}")
    gambar_komparasi(agg_sari, hasil_sari,
                     "Perbandingan 5 Metode Defuzzifikasi (Sari Dewi)", "hasil/p8_komparasi_sari.png")

    # --- Semua data uji
    data = [("Budi Santoso", 25, 20), ("Sari Dewi", 45, 35), ("Ahmad Fauzi", 60, 65),
            ("Rina Marlina", 80, 85), ("Dodi Pratama", 55, 45)]
    print("\nSEMUA DATA UJI")
    print(f"{'Nama':<14}" + "".join(f"{m.upper():>10}" for m in METODE))
    for nama, p, d in data:
        agg = agregasi_mamdani(alpha_per_label_dari_aturan(hitung_alpha_aturan(p, d)))
        print(f"{nama:<14}" + "".join(f"{defuzz(agg, m):>10.2f}" for m in METODE))
