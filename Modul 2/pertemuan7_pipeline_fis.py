from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


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
# 2. KELAS FUZZY INFERENCE SYSTEM
# ==========================================================
class FuzzyInferenceSystem:
    def __init__(self):
        self.inputs = {}      # nama -> (universe, {label: fungsi})
        self.output = None    # (nama, universe, {label: fungsi})
        self.rules = []       # list of (antecedent_dict, label_output)
        self.detail = {}      # hasil tahapan terakhir (untuk visualisasi)

    def add_input_variable(self, name, universe, mf_dict):
        self.inputs[name] = (np.asarray(universe, dtype=float), mf_dict)

    def set_output_variable(self, name, universe, mf_dict):
        self.output = (name, np.asarray(universe, dtype=float), mf_dict)

    def add_rule(self, rule_tuple):
        """rule_tuple = ({'produktivitas': 'Sedang', 'kedisiplinan': 'Tinggi'}, 'Baik')"""
        self.rules.append(rule_tuple)

    # --- Tahap 1: fuzzifikasi
    def fuzzifikasi(self, input_values):
        derajat = {}
        for nama, (semesta, mf_dict) in self.inputs.items():
            x = float(np.clip(input_values[nama], semesta.min(), semesta.max()))
            derajat[nama] = {lbl: float(f(x)) for lbl, f in mf_dict.items()}
        return derajat

    # --- Tahap 2: evaluasi aturan (AND = min)
    def evaluasi_aturan(self, derajat):
        alphas = []
        for antecedent, _ in self.rules:
            alphas.append(min(derajat[var][lbl] for var, lbl in antecedent.items()))
        return alphas

    # --- Tahap 3 dan 4: implikasi (min) lalu agregasi (max)
    def implikasi_agregasi(self, alphas):
        _, z, mf_out = self.output
        agregasi = np.zeros_like(z)
        terpotong = []
        for alpha, (_, lbl_out) in zip(alphas, self.rules):
            potong = np.minimum(alpha, mf_out[lbl_out](z))
            terpotong.append(potong)
            agregasi = np.maximum(agregasi, potong)
        return terpotong, agregasi

    # --- Tahap 5: defuzzifikasi centroid (dengan fallback)
    def defuzzifikasi(self, agregasi):
        _, z, _ = self.output
        total = np.sum(agregasi)
        if total == 0:
            print("PERINGATAN: semua alpha = 0, memakai titik tengah semesta output")
            return float((z.min() + z.max()) / 2)
        return float(np.sum(z * agregasi) / total)

    def compute(self, input_values):
        derajat = self.fuzzifikasi(input_values)
        alphas = self.evaluasi_aturan(derajat)
        terpotong, agregasi = self.implikasi_agregasi(alphas)
        crisp = self.defuzzifikasi(agregasi)
        self.detail = {"derajat": derajat, "alphas": alphas,
                       "terpotong": terpotong, "agregasi": agregasi, "crisp": crisp}
        return crisp


# ==========================================================
# 3. MEMBANGUN SISTEM (parameter dan aturan dari asesmen)
# ==========================================================
def bangun_fis():
    fis = FuzzyInferenceSystem()
    semesta = np.linspace(0, 100, 1001)
    mf_input = {
        "Rendah": lambda x: trapesium(x, 0, 0, 30, 50),
        "Sedang": lambda x: segitiga(x, 30, 50, 70),
        "Tinggi": lambda x: trapesium(x, 50, 70, 100, 100),
    }
    mf_output = {
        "Buruk": lambda x: trapesium(x, 0, 0, 20, 40),
        "Cukup": lambda x: segitiga(x, 20, 40, 60),
        "Baik": lambda x: segitiga(x, 40, 60, 80),
        "Sangat Baik": lambda x: trapesium(x, 60, 80, 100, 100),
    }
    fis.add_input_variable("produktivitas", semesta, mf_input)
    fis.add_input_variable("kedisiplinan", semesta, mf_input)
    fis.set_output_variable("kinerja", semesta, mf_output)

    aturan = [
        ("Rendah", "Rendah", "Buruk"), ("Rendah", "Sedang", "Cukup"),
        ("Rendah", "Tinggi", "Cukup"), ("Sedang", "Rendah", "Cukup"),
        ("Sedang", "Sedang", "Baik"),  ("Sedang", "Tinggi", "Baik"),
        ("Tinggi", "Rendah", "Cukup"), ("Tinggi", "Sedang", "Baik"),
        ("Tinggi", "Tinggi", "Sangat Baik"),
    ]
    for p, d, k in aturan:
        fis.add_rule(({"produktivitas": p, "kedisiplinan": d}, k))
    return fis


# ==========================================================
# 4. VISUALISASI PIPELINE
# ==========================================================
def gambar_pipeline(fis, nama_file):
    _, z, mf_out = fis.output
    det = fis.detail
    warna = {"Buruk": "tab:red", "Cukup": "tab:orange", "Baik": "tab:blue", "Sangat Baik": "tab:green"}

    plt.figure(figsize=(11, 5.5))
    for lbl, f in mf_out.items():
        plt.plot(z, f(z), "--", color=warna[lbl], alpha=0.5, label=f"MF {lbl}")
    plt.fill_between(z, 0, det["agregasi"], color="purple", alpha=0.35, label="Daerah agregasi")
    plt.plot(z, det["agregasi"], color="purple", linewidth=2.5)
    plt.axvline(det["crisp"], color="black", linewidth=2.2,
                label=f"Centroid = {det['crisp']:.2f}")
    plt.title("Pipeline FIS: Implikasi, Agregasi, dan Defuzzifikasi Centroid", fontweight="bold")
    plt.xlabel("Kinerja Karyawan")
    plt.ylabel("Derajat keanggotaan")
    plt.ylim(-0.05, 1.05)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left", fontsize=9)
    plt.tight_layout()
    Path(nama_file).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(nama_file, dpi=200)
    plt.close()


# ==========================================================
# 5. PENGUJIAN
# ==========================================================
if __name__ == "__main__":
    fis = bangun_fis()

    # Contoh alur lengkap (Ahmad Fauzi)
    z_crisp = fis.compute({"produktivitas": 60, "kedisiplinan": 65})
    det = fis.detail
    print("Fuzzifikasi :", det["derajat"])
    print("Alpha aktif :", [(f"R{i+1}", a) for i, a in enumerate(det["alphas"]) if a > 0])
    print(f"Centroid    : {z_crisp:.2f}")
    gambar_pipeline(fis, "hasil/p7_pipeline_ahmad.png")

    # Tugas 7: 3 kasus uji
    kasus = [("Kasus 1", 25, 20), ("Kasus 2", 60, 65), ("Kasus 3", 80, 85)]
    print("\nHASIL TUGAS 7")
    for nama, p, d in kasus:
        hasil = fis.compute({"produktivitas": p, "kedisiplinan": d})
        print(f"{nama}: Produktivitas={p}, Kedisiplinan={d} -> Kinerja = {hasil:.2f}")
