import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ==========================================================
# 1. FUZZIFIKASI DAN FIRING STRENGTH (dari Praktikum 6)
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


def mf_input(x):
    return {"Rendah": float(trapesium(x, 0, 0, 30, 50)),
            "Sedang": float(segitiga(x, 30, 50, 70)),
            "Tinggi": float(trapesium(x, 50, 70, 100, 100))}


# Basis aturan asesmen: (Produktivitas, Kedisiplinan, Kinerja)
RULES = [("Rendah", "Rendah", "Buruk"), ("Rendah", "Sedang", "Cukup"), ("Rendah", "Tinggi", "Cukup"),
         ("Sedang", "Rendah", "Cukup"), ("Sedang", "Sedang", "Baik"), ("Sedang", "Tinggi", "Baik"),
         ("Tinggi", "Rendah", "Cukup"), ("Tinggi", "Sedang", "Baik"), ("Tinggi", "Tinggi", "Sangat Baik")]


def hitung_alphas(p, d):
    fp, fd = mf_input(p), mf_input(d)
    return [min(fp[a], fd[b]) for a, b, _ in RULES]


# ==========================================================
# 2. SUGENO (ORDE 0 DAN ORDE 1)
# ==========================================================
def hitung_sugeno(alphas, z_values):
    alphas = np.array(alphas, dtype=float)
    z_values = np.array(z_values, dtype=float)
    total = alphas.sum()
    return 0.0 if total == 0 else float(np.sum(alphas * z_values) / total)


# Orde 0: konstanta tiap konsekuen (titik tengah himpunan output asesmen)
KONSTANTA = {"Buruk": 10.0, "Cukup": 40.0, "Baik": 60.0, "Sangat Baik": 90.0}

# Orde 1: z = p*Produktivitas + q*Kedisiplinan + r  (koefisien untuk demonstrasi)
KOEF_ORDE1 = {"Buruk": (0.4, 0.4, -5.0), "Cukup": (0.4, 0.4, 5.0),
              "Baik": (0.4, 0.4, 15.0), "Sangat Baik": (0.4, 0.4, 25.0)}


def sugeno_orde0(p, d):
    alphas = hitung_alphas(p, d)
    z_values = [KONSTANTA[k] for _, _, k in RULES]
    return hitung_sugeno(alphas, z_values), alphas, z_values


def sugeno_orde1(p, d):
    alphas = hitung_alphas(p, d)
    z_values = []
    for _, _, k in RULES:
        a, b, c = KOEF_ORDE1[k]
        z_values.append(min(100.0, max(0.0, a * p + b * d + c)))   # dibatasi 0-100
    return hitung_sugeno(alphas, z_values), alphas, z_values


# ==========================================================
# 3. TSUKAMOTO (KONSEKUEN MONOTON)
# ==========================================================
def invers_monoton_naik(alpha, a, b):
    """z = a + alpha * (b - a)"""
    return a + alpha * (b - a)


def invers_monoton_turun(alpha, a, b):
    """z = b - alpha * (b - a)"""
    return b - alpha * (b - a)


# Konsekuen monoton: sisi monoton dari himpunan output asesmen
FUNGSI_TSUKAMOTO = {
    "Buruk": lambda al: invers_monoton_turun(al, 20.0, 40.0),
    "Cukup": lambda al: invers_monoton_naik(al, 20.0, 40.0),
    "Baik": lambda al: invers_monoton_naik(al, 40.0, 60.0),
    "Sangat Baik": lambda al: invers_monoton_naik(al, 60.0, 80.0),
}


def hitung_tsukamoto(p, d):
    alphas = hitung_alphas(p, d)
    z_values = [FUNGSI_TSUKAMOTO[k](a) for a, (_, _, k) in zip(alphas, RULES)]
    return hitung_sugeno(alphas, z_values), alphas, z_values


# ==========================================================
# 4. MAMDANI (CENTROID) SEBAGAI PEMBANDING
# ==========================================================
Z = np.linspace(0, 100, 1001)
MF_OUT = {"Buruk": trapesium(Z, 0, 0, 20, 40), "Cukup": segitiga(Z, 20, 40, 60),
          "Baik": segitiga(Z, 40, 60, 80), "Sangat Baik": trapesium(Z, 60, 80, 100, 100)}


def mamdani_centroid(p, d):
    agg = np.zeros_like(Z)
    for alpha, (_, _, k) in zip(hitung_alphas(p, d), RULES):
        agg = np.fmax(agg, np.fmin(alpha, MF_OUT[k]))
    return float(np.sum(Z * agg) / np.sum(agg))


# ==========================================================
# 5. PENGUJIAN DAN KOMPARASI
# ==========================================================
if __name__ == "__main__":
    # Contoh perhitungan: Ahmad Fauzi
    s0, al, zs0 = sugeno_orde0(60, 65)
    s1, _, zs1 = sugeno_orde1(60, 65)
    ts, _, zts = hitung_tsukamoto(60, 65)
    aktif = [i for i, a in enumerate(al) if a > 0]
    print("CONTOH AHMAD FAUZI (60, 65)")
    for i in aktif:
        print(f"  R{i+1}: alpha={al[i]:.2f}  z_sugeno0={zs0[i]:.1f}  z_sugeno1={zs1[i]:.1f}  z_tsukamoto={zts[i]:.1f}")
    print(f"  Sugeno orde 0 = {s0:.3f} | Sugeno orde 1 = {s1:.3f} | Tsukamoto = {ts:.3f}")

    # Tugas 9: 5 data uji
    data = [("Budi Santoso", 25, 20), ("Sari Dewi", 45, 35), ("Ahmad Fauzi", 60, 65),
            ("Rina Marlina", 80, 85), ("Dodi Pratama", 55, 45)]
    print("\nTUGAS 9: PERBANDINGAN HASIL")
    print(f"{'Nama':<14}{'Mamdani':>9}{'Sugeno0':>9}{'Sugeno1':>9}{'Tsukamoto':>11}{'S0-M':>8}{'T-M':>8}{'T-S0':>8}")
    baris = []
    for nama, p, d in data:
        m = mamdani_centroid(p, d)
        a = sugeno_orde0(p, d)[0]
        b = sugeno_orde1(p, d)[0]
        t = hitung_tsukamoto(p, d)[0]
        baris.append((nama, m, a, b, t))
        print(f"{nama:<14}{m:>9.2f}{a:>9.2f}{b:>9.2f}{t:>11.2f}{a-m:>8.2f}{t-m:>8.2f}{t-a:>8.2f}")

    # Grafik perbandingan
    x = np.arange(len(baris))
    lebar = 0.2
    plt.figure(figsize=(11, 5.5))
    for k, (judul, warna) in enumerate([("Mamdani", "tab:blue"), ("Sugeno orde 0", "tab:orange"),
                                        ("Sugeno orde 1", "tab:green"), ("Tsukamoto", "tab:red")]):
        plt.bar(x + (k - 1.5) * lebar, [b[k + 1] for b in baris], lebar, label=judul, color=warna)
    plt.xticks(x, [b[0].split()[0] for b in baris])
    plt.ylabel("Nilai Kinerja")
    plt.title("Perbandingan Mamdani, Sugeno, dan Tsukamoto", fontweight="bold")
    plt.grid(axis="y", linestyle=":", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig("hasil/p9_perbandingan_metode.png", dpi=200)
    plt.close()
