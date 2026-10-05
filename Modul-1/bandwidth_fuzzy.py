import numpy as np
import matplotlib.pyplot as plt

# 1. DEFINISI FUNGSI KEANGGOTAAN
def mf_bandwidth_a(x):
    """Segitiga [30, 60, 90]"""
    return np.maximum(0.0, np.minimum((x - 30.0) / 30.0, (90.0 - x) / 30.0))

def mf_packet_loss_b(x):
    """Trapesium [40, 55, 75, 95]"""
    term1 = (x - 40.0) / 15.0
    term2 = (95.0 - x) / 20.0
    return np.maximum(0.0, np.minimum(term1, np.minimum(1.0, term2)))

# 2. OPERATOR LOGIKA FUZZY
def tnorm_min(a, b): return np.minimum(a, b)
def tnorm_product(a, b): return a * b
def tconorm_max(a, b): return np.maximum(a, b)
def tconorm_algebraic_sum(a, b): return a + b - (a * b)
def fuzzy_not(a): return 1.0 - a

# 3. DOMAIN SEMESTA X = [0, 100]
x = np.linspace(0, 100, 1000)
mu_a = mf_bandwidth_a(x)
mu_b = mf_packet_loss_b(x)

# 4. PLOTTING OPERASI FUZZY
fig, axes = plt.subplots(2, 2, figsize=(13, 8))

# Plot 1: Himpunan Dasar A, B, dan NOT A
axes[0, 0].plot(x, mu_a, label='Himpunan A (Bandwidth)', color='blue', linewidth=2)
axes[0, 0].plot(x, mu_b, label='Himpunan B (Packet Loss)', color='orange', linewidth=2)
axes[0, 0].plot(x, fuzzy_not(mu_a), label='NOT A (Komplemen)', color='gray', linestyle='--', linewidth=1.5)
axes[0, 0].set_title('1. Himpunan A, B, dan Komplemen NOT A')
axes[0, 0].grid(True, alpha=0.5)
axes[0, 0].legend()

# Plot 2: Irisan (AND)
axes[0, 1].plot(x, tnorm_min(mu_a, mu_b), label='Zadeh Min (AND)', color='green', linewidth=2)
axes[0, 1].plot(x, tnorm_product(mu_a, mu_b), label='Algebraic Product (AND)', color='red', linestyle='-.', linewidth=2)
axes[0, 1].set_title('2. Operasi Irisan (Intersection / AND)')
axes[0, 1].grid(True, alpha=0.5)
axes[0, 1].legend()

# Plot 3: Gabungan (OR)
axes[1, 0].plot(x, tconorm_max(mu_a, mu_b), label='Zadeh Max (OR)', color='green', linewidth=2)
axes[1, 0].plot(x, tconorm_algebraic_sum(mu_a, mu_b), label='Algebraic Sum (OR)', color='red', linestyle='-.', linewidth=2)
axes[1, 0].set_title('3. Operasi Gabungan (Union / OR)')
axes[1, 0].grid(True, alpha=0.5)
axes[1, 0].legend()

# Plot 4: Area Irisan vs Gabungan
axes[1, 1].fill_between(x, tnorm_min(mu_a, mu_b), color='green', alpha=0.3, label='Area Zadeh Min')
axes[1, 1].plot(x, tconorm_max(mu_a, mu_b), color='red', linewidth=2, label='Batas Zadeh Max')
axes[1, 1].set_title('4. Perbandingan Area Min vs Max')
axes[1, 1].grid(True, alpha=0.5)
axes[1, 1].legend()

plt.tight_layout()
plt.show()

# 5. PENGUJIAN TEPAT PADA 4 POINT THROUGHPUT
titik_uji = [35.0, 50.0, 65.0, 80.0]

print("=" * 90)
print(f"{'Throughput':<12} | {'μ_A':<8} | {'μ_B':<8} | {'Zadeh Min':<10} | {'Alg Prod':<10} | {'Zadeh Max':<10} | {'Alg Sum':<10} | {'NOT A':<8}")
print("=" * 90)

for val in titik_uji:
    a = mf_bandwidth_a(val)
    b = mf_packet_loss_b(val)
    print(f"{val:<12.1f} | {a:<8.4f} | {b:<8.4f} | {tnorm_min(a, b):<10.4f} | {tnorm_product(a, b):<10.4f} | {tconorm_max(a, b):<10.4f} | {tconorm_algebraic_sum(a, b):<10.4f} | {fuzzy_not(a):<8.4f}")

print("=" * 90)