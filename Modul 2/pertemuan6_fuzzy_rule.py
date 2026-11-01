# ==========================================================
# 1. FUNGSI KEANGGOTAAN (rumus dan parameter sesuai asesmen)
# ==========================================================
def trapesium(x, a, b, c, d):
    """Trapesium [a, b, c, d]. Jika a == b atau c == d, bagian itu jadi 'bahu' (nilai 1 di tepi)."""
    if x < a or x > d:
        return 0.0
    if b <= x <= c:
        return 1.0
    if x < b:
        return (x - a) / (b - a)
    return (d - x) / (d - c)


def segitiga(x, a, b, c):
    """Segitiga [a, b, c]"""
    if x <= a or x >= c:
        return 0.0
    if x <= b:
        return (x - a) / (b - a)
    return (c - x) / (c - b)


# ==========================================================
# 2. DATABASE FUNGSI KEANGGOTAAN (INPUT)
# ==========================================================
MF_INPUT = {
    "produktivitas": {
        "Rendah": lambda x: trapesium(x, 0, 0, 30, 50),
        "Sedang": lambda x: segitiga(x, 30, 50, 70),
        "Tinggi": lambda x: trapesium(x, 50, 70, 100, 100),
    },
    "kedisiplinan": {
        "Rendah": lambda x: trapesium(x, 0, 0, 30, 50),
        "Sedang": lambda x: segitiga(x, 30, 50, 70),
        "Tinggi": lambda x: trapesium(x, 50, 70, 100, 100),
    },
}


def fuzzifikasi(produktivitas, kedisiplinan):
    """Mengubah nilai crisp menjadi derajat keanggotaan tiap label."""
    nilai = {"produktivitas": produktivitas, "kedisiplinan": kedisiplinan}
    return {
        var: {label: mf(nilai[var]) for label, mf in labels.items()}
        for var, labels in MF_INPUT.items()
    }


# ==========================================================
# 3. KELAS STRUKTUR ATURAN FUZZY
# ==========================================================
class FuzzyRule:
    def __init__(self, rule_id, antecedent, consequent, operator="AND"):
        self.rule_id = rule_id
        self.antecedent = antecedent
        self.consequent = consequent
        self.operator = operator.upper()

    def hitung_firing_strength(self, derajat_fuzzifikasi):
        nilai_derajat = []
        for var_nama, label_nama in self.antecedent.items():
            deg = derajat_fuzzifikasi[var_nama].get(label_nama, 0.0)
            nilai_derajat.append(deg)

        if not nilai_derajat:
            return 0.0
        if self.operator == "AND":
            return min(nilai_derajat)
        elif self.operator == "OR":
            return max(nilai_derajat)
        raise ValueError(f"Operator {self.operator} tidak dikenali.")

    def __str__(self):
        syarat = f" {self.operator} ".join(
            f"{var} is {lbl}" for var, lbl in self.antecedent.items())
        hasil = ", ".join(f"{var} is {lbl}" for var, lbl in self.consequent.items())
        return f"[{self.rule_id}] IF {syarat} THEN {hasil}"


# ==========================================================
# 4. BASIS ATURAN (RULE BASE) - 9 ATURAN DARI ASESMEN
# ==========================================================
def buat_rule(rid, p, d, k):
    return FuzzyRule(rid, {"produktivitas": p, "kedisiplinan": d}, {"kinerja": k})

rule_base = [
    buat_rule("R1", "Rendah", "Rendah", "Buruk"),
    buat_rule("R2", "Rendah", "Sedang", "Cukup"),
    buat_rule("R3", "Rendah", "Tinggi", "Cukup"),
    buat_rule("R4", "Sedang", "Rendah", "Cukup"),
    buat_rule("R5", "Sedang", "Sedang", "Baik"),
    buat_rule("R6", "Sedang", "Tinggi", "Baik"),
    buat_rule("R7", "Tinggi", "Rendah", "Cukup"),
    buat_rule("R8", "Tinggi", "Sedang", "Baik"),
    buat_rule("R9", "Tinggi", "Tinggi", "Sangat Baik"),
]


# ==========================================================
# 5. EVALUASI ATURAN
# ==========================================================
def evaluasi_aturan(derajat, tampil_semua=True):
    aturan_aktif = []
    for rule in rule_base:
        alpha = rule.hitung_firing_strength(derajat)
        lbl = rule.consequent["kinerja"]
        status = f"AKTIF (alpha = {alpha:.2f})" if alpha > 0 else "NONAKTIF"
        if tampil_semua:
            print(f"  {rule} --> {status}")
        if alpha > 0:
            aturan_aktif.append((rule.rule_id, lbl, alpha))
    return aturan_aktif


def tampilkan_hasil(nama, p, d):
    print("=" * 78)
    print(f"{nama}  (Produktivitas = {p}, Kedisiplinan = {d})")
    print("=" * 78)
    derajat = fuzzifikasi(p, d)
    for var, labels in derajat.items():
        teks = ", ".join(f"{k}={v:.2f}" for k, v in labels.items())
        print(f"  Fuzzifikasi {var:<14}: {teks}")
    print("  Evaluasi 9 aturan:")
    aktif = evaluasi_aturan(derajat)
    print("  Ringkasan aturan yang terpicu:")
    for rid, lbl, alpha in aktif:
        print(f"   - {rid:<3}: Kinerja = {lbl:<12} alpha = {alpha:.2f}")
    print()
    return aktif


# ==========================================================
# 6. PENGUJIAN: 5 DATA SIMULASI DARI ASESMEN
# ==========================================================
data_uji = [
    ("Budi Santoso", 25, 20),
    ("Sari Dewi",    45, 35),
    ("Ahmad Fauzi",  60, 65),
    ("Rina Marlina", 80, 85),
    ("Dodi Pratama", 55, 45),
]

if __name__ == "__main__":
    for nama, p, d in data_uji:
        tampilkan_hasil(nama, p, d)
