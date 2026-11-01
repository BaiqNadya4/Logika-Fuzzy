import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


# ==========================================================
# 1. FUNGSI KEANGGOTAAN (rumus dan parameter sesuai asesmen)
# ==========================================================
def trapesium(x, a, b, c, d):
    x_in = np.asarray(x, dtype=float)
    x = np.atleast_1d(x_in)
    y = np.zeros_like(x)
    if b > a:
        m = (x > a) & (x < b)
        y[m] = (x[m] - a) / (b - a)
    y[(x >= b) & (x <= c)] = 1.0
    if d > c:
        m = (x > c) & (x < d)
        y[m] = (d - x[m]) / (d - c)
    return float(y[0]) if x_in.ndim == 0 else y


def segitiga(x, a, b, c):
    x_in = np.asarray(x, dtype=float)
    x = np.atleast_1d(x_in)
    y = np.zeros_like(x)
    m = (x > a) & (x <= b)
    y[m] = (x[m] - a) / (b - a)
    m = (x > b) & (x < c)
    y[m] = (c - x[m]) / (c - b)
    return float(y[0]) if x_in.ndim == 0 else y


# ==========================================================
# 2. MODEL VARIABEL FUZZY (REVIEW MODUL 1)
# ==========================================================
MF_INPUT = {
    "Rendah": lambda x: trapesium(x, 0, 0, 30, 50),
    "Sedang": lambda x: segitiga(x, 30, 50, 70),
    "Tinggi": lambda x: trapesium(x, 50, 70, 100, 100),
}
MF_OUTPUT = {
    "Buruk": lambda x: trapesium(x, 0, 0, 20, 40),
    "Cukup": lambda x: segitiga(x, 20, 40, 60),
    "Baik": lambda x: segitiga(x, 40, 60, 80),
    "Sangat Baik": lambda x: trapesium(x, 60, 80, 100, 100),
}
SEMESTA_OUT = np.linspace(0, 100, 1001)
MU_OUTPUT = {lbl: f(SEMESTA_OUT) for lbl, f in MF_OUTPUT.items()}

# ==========================================================
# 3. BASIS ATURAN (9 ATURAN, MATRIKS 3 x 3)
# ==========================================================
RULE_BASE = [
    ("R1", "Rendah", "Rendah", "Buruk"),
    ("R2", "Rendah", "Sedang", "Cukup"),
    ("R3", "Rendah", "Tinggi", "Cukup"),
    ("R4", "Sedang", "Rendah", "Cukup"),
    ("R5", "Sedang", "Sedang", "Baik"),
    ("R6", "Sedang", "Tinggi", "Baik"),
    ("R7", "Tinggi", "Rendah", "Cukup"),
    ("R8", "Tinggi", "Sedang", "Baik"),
    ("R9", "Tinggi", "Tinggi", "Sangat Baik"),
]


# ==========================================================
# 4. MESIN INFERENSI MAMDANI
# ==========================================================
def fuzzifikasi(nilai):
    return {lbl: float(f(nilai)) for lbl, f in MF_INPUT.items()}


def evaluasi_aturan(mu_p, mu_d):
    """AND = minimum. Mengembalikan list (id, label_output, alpha)."""
    return [(rid, out, min(mu_p[lp], mu_d[ld])) for rid, lp, ld, out in RULE_BASE]


def implikasi_agregasi(hasil_aturan):
    agregasi = np.zeros_like(SEMESTA_OUT)
    for _, out, alpha in hasil_aturan:
        if alpha > 0:
            agregasi = np.fmax(agregasi, np.fmin(alpha, MU_OUTPUT[out]))   # implikasi min, agregasi max
    return agregasi


def defuzzifikasi_centroid(agregasi):
    total = np.sum(agregasi)
    if total == 0:
        return 0.0
    return float(np.sum(SEMESTA_OUT * agregasi) / total)


def kategori(nilai):
    if nilai < 40:
        return "Buruk"
    if nilai < 60:
        return "Cukup"
    if nilai < 80:
        return "Baik"
    return "Sangat Baik"


def evaluasi_sistem_fuzzy(produktivitas, kedisiplinan, detail=False):
    mu_p = fuzzifikasi(produktivitas)
    mu_d = fuzzifikasi(kedisiplinan)
    hasil_aturan = evaluasi_aturan(mu_p, mu_d)
    agregasi = implikasi_agregasi(hasil_aturan)
    crisp = defuzzifikasi_centroid(agregasi)
    if detail:
        return {"mu_p": mu_p, "mu_d": mu_d, "aturan": hasil_aturan,
                "agregasi": agregasi, "crisp": crisp, "kategori": kategori(crisp)}
    return crisp


# ==========================================================
# 5. PENGUJIAN
# ==========================================================
DATA_UJI = [
    ("Budi Santoso", 25, 20),
    ("Sari Dewi", 45, 35),
    ("Ahmad Fauzi", 60, 65),
    ("Rina Marlina", 80, 85),
    ("Dodi Pratama", 55, 45),
]
DATA_EKSTREM = [("Ekstrem rendah", 0, 0), ("Ekstrem tinggi", 100, 100),
                ("Produktif, tidak disiplin", 100, 0), ("Disiplin, tidak produktif", 0, 100)]


def jalankan_pengujian(data, judul):
    print("=" * 86)
    print(judul)
    print("=" * 86)
    for nama, p, d in data:
        h = evaluasi_sistem_fuzzy(p, d, detail=True)
        aktif = ", ".join(f"{rid}={a:.2f}" for rid, _, a in h["aturan"] if a > 0)
        print(f"{nama:<26} P={p:<4} D={d:<4} -> {h['crisp']:6.2f} ({h['kategori']:<11}) aturan aktif: {aktif}")


# ==========================================================
# 6. VISUALISASI
# ==========================================================
def plot_fungsi_keanggotaan(nama_file):
    x = SEMESTA_OUT
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
    for lbl, f in MF_INPUT.items():
        ax[0].plot(x, f(x), linewidth=2, label=lbl)
    ax[0].set_title("Produktivitas dan Kedisiplinan (input)", fontweight="bold")
    for lbl, f in MF_OUTPUT.items():
        ax[1].plot(x, f(x), linewidth=2, label=lbl)
    ax[1].set_title("Kinerja Karyawan (output)", fontweight="bold")
    for a in ax:
        a.set_xlabel("Nilai (0-100)")
        a.set_ylabel("Derajat keanggotaan")
        a.set_ylim(-0.05, 1.05)
        a.grid(True, linestyle=":", alpha=0.6)
        a.legend()
    plt.tight_layout()
    plt.savefig(nama_file, dpi=200)
    plt.close()


def plot_agregasi(p, d, nama_file):
    h = evaluasi_sistem_fuzzy(p, d, detail=True)
    plt.figure(figsize=(10, 5))
    for lbl in MU_OUTPUT:
        plt.plot(SEMESTA_OUT, MU_OUTPUT[lbl], "--", alpha=0.45, label=f"MF {lbl}")
    plt.fill_between(SEMESTA_OUT, 0, h["agregasi"], color="purple", alpha=0.35, label="Agregasi")
    plt.plot(SEMESTA_OUT, h["agregasi"], color="purple", linewidth=2.5)
    plt.axvline(h["crisp"], color="black", linewidth=2.2, label=f"Centroid = {h['crisp']:.2f}")
    plt.title(f"Kurva Agregasi (Produktivitas={p}, Kedisiplinan={d})", fontweight="bold")
    plt.xlabel("Kinerja Karyawan")
    plt.ylabel("Derajat keanggotaan")
    plt.ylim(-0.05, 1.05)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    plt.savefig(nama_file, dpi=200)
    plt.close()


def plot_decision_surface(nama_file):
    x1 = np.linspace(0, 100, 30)
    x2 = np.linspace(0, 100, 30)
    X1, X2 = np.meshgrid(x1, x2)
    Z_out = np.zeros_like(X1)
    for i in range(X1.shape[0]):
        for j in range(X1.shape[1]):
            Z_out[i, j] = evaluasi_sistem_fuzzy(X1[i, j], X2[i, j])
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X1, X2, Z_out, cmap="viridis", edgecolor="none", alpha=0.9)
    ax.set_xlabel("Produktivitas")
    ax.set_ylabel("Kedisiplinan")
    ax.set_zlabel("Kinerja Karyawan")
    ax.set_title("Decision Surface Sistem Fuzzy Kinerja Karyawan", fontweight="bold")
    ax.view_init(elev=28, azim=-125)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig(nama_file, dpi=200)
    plt.close()
    return Z_out


# ==========================================================
# 7. PROGRAM UTAMA
# ==========================================================
def input_angka(pesan):
    while True:
        try:
            nilai = float(input(pesan))
            if 0 <= nilai <= 100:
                return nilai
            print("Nilai harus di antara 0 sampai 100.")
        except ValueError:
            print("Masukkan angka yang valid.")


if __name__ == "__main__":
    if "--uji" in sys.argv:
        os.makedirs("hasil", exist_ok=True)
        jalankan_pengujian(DATA_UJI, "PENGUJIAN 5 DATA UJI")
        jalankan_pengujian(DATA_EKSTREM, "PENGUJIAN TAMBAHAN: NILAI EKSTREM")
        plot_fungsi_keanggotaan("hasil/p10_fungsi_keanggotaan.png")
        plot_agregasi(60, 65, "hasil/p10_agregasi_ahmad.png")
        Z_out = plot_decision_surface("hasil/p10_decision_surface.png")
        print(f"\nDecision surface: min = {Z_out.min():.2f}, maks = {Z_out.max():.2f}")
    else:
        print("SISTEM PENENTUAN KINERJA KARYAWAN (FUZZY MAMDANI)")
        p = input_angka("Produktivitas (0-100): ")
        d = input_angka("Kedisiplinan  (0-100): ")
        h = evaluasi_sistem_fuzzy(p, d, detail=True)
        print("Aturan aktif:", ", ".join(f"{r}={a:.2f}" for r, _, a in h["aturan"] if a > 0))
        print(f"Nilai kinerja = {h['crisp']:.2f}  -> kategori: {h['kategori']}")
