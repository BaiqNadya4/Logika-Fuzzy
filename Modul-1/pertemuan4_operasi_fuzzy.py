import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. IMPLEMENTASI OPERATOR T-NORM (AND)
# ==========================================================
def tnorm_min(mu_a, mu_b):
    """Zadeh Min: min(A, B)"""
    return np.minimum(mu_a, mu_b)


def tnorm_product(mu_a, mu_b):
    """Algebraic Product: A * B"""
    return mu_a * mu_b


def tnorm_bounded_diff(mu_a, mu_b):
    """Bounded Difference: max(0, A + B - 1)"""
    return np.maximum(0.0, mu_a + mu_b - 1.0)


# ==========================================================
# 2. IMPLEMENTASI OPERATOR T-CONORM (OR)
# ==========================================================
def tconorm_max(mu_a, mu_b):
    """Zadeh Max: max(A, B)"""
    return np.maximum(mu_a, mu_b)


def tconorm_algebraic_sum(mu_a, mu_b):
    """Algebraic Sum: A + B - (A * B)"""
    return mu_a + mu_b - (mu_a * mu_b)


def tconorm_bounded_sum(mu_a, mu_b):
    """Bounded Sum: min(1, A + B)"""
    return np.minimum(1.0, mu_a + mu_b)


# ==========================================================
# 3. IMPLEMENTASI KOMPLEMEN (NOT)
# ==========================================================
def fuzzy_not(mu):
    """Zadeh Complement: 1 - mu"""
    return 1.0 - mu


# ==========================================================
# 4. SIMULASI DUA FUNGSI KEANGGOTAAN
# ==========================================================
x = np.linspace(0, 10, 500)

# Himpunan A: Segitiga di kiri [1, 3, 6]
mu_a = np.maximum(0.0, np.minimum((x - 1.0) / (3.0 - 1.0), (6.0 - x) / (6.0 - 3.0)))

# Himpunan B: Segitiga di kanan [4, 7, 9]
mu_b = np.maximum(0.0, np.minimum((x - 4.0) / (7.0 - 4.0), (9.0 - x) / (9.0 - 7.0)))


# ==========================================================
# 5. VISUALISASI KOMPARASI OPERASI
# ==========================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 9))

# Panel 1: Himpunan Dasar A, B dan Not A
axes[0, 0].plot(x, mu_a, label='Himpunan A', color='#1f77b4', linewidth=2.5)
axes[0, 0].plot(x, mu_b, label='Himpunan B', color='#ff7f0e', linewidth=2.5)
axes[0, 0].plot(x, fuzzy_not(mu_a), label='NOT A (Komplemen)', color='gray', linestyle='--', linewidth=1.8)
axes[0, 0].set_title('1. Himpunan A, B, dan Komplemen NOT A', fontweight='bold')
axes[0, 0].set_ylim(-0.05, 1.1)
axes[0, 0].grid(True, linestyle=':', alpha=0.6)
axes[0, 0].legend()

# Panel 2: Komparasi Operator Intersection (T-Norm)
axes[0, 1].plot(x, tnorm_min(mu_a, mu_b), label='Zadeh Min (Standar)', color='#2ca02c', linewidth=2.5)
axes[0, 1].plot(x, tnorm_product(mu_a, mu_b), label='Algebraic Product', color='#d62728', linestyle='-.', linewidth=2)
axes[0, 1].plot(x, tnorm_bounded_diff(mu_a, mu_b), label='Bounded Diff', color='#9467bd', linestyle=':', linewidth=2)
axes[0, 1].set_title('2. Operasi Intersection (AND / T-Norm)', fontweight='bold')
axes[0, 1].set_ylim(-0.05, 1.1)
axes[0, 1].grid(True, linestyle=':', alpha=0.6)
axes[0, 1].legend()

# Panel 3: Komparasi Operator Union (T-Conorm)
axes[1, 0].plot(x, tconorm_max(mu_a, mu_b), label='Zadeh Max (Standar)', color='#2ca02c', linewidth=2.5)
axes[1, 0].plot(x, tconorm_algebraic_sum(mu_a, mu_b), label='Algebraic Sum', color='#d62728', linestyle='-.', linewidth=2)
axes[1, 0].plot(x, tconorm_bounded_sum(mu_a, mu_b), label='Bounded Sum', color='#9467bd', linestyle=':', linewidth=2)
axes[1, 0].set_title('3. Operasi Union (OR / T-Conorm)', fontweight='bold')
axes[1, 0].set_ylim(-0.05, 1.1)
axes[1, 0].grid(True, linestyle=':', alpha=0.6)
axes[1, 0].legend()

# Panel 4: Perbandingan Daerah Area Min vs Max
axes[1, 1].fill_between(x, tnorm_min(mu_a, mu_b), color='#2ca02c', alpha=0.4, label='Area Min (A ∩ B)')
axes[1, 1].plot(x, tconorm_max(mu_a, mu_b), color='#d62728', linewidth=2, label='Batas Max (A ∪ B)')
axes[1, 1].plot(x, mu_a, color='#1f77b4', linestyle=':', alpha=0.7)
axes[1, 1].plot(x, mu_b, color='#ff7f0e', linestyle=':', alpha=0.7)
axes[1, 1].set_title('4. Hubungan Area Irisan vs Gabungan Standar', fontweight='bold')
axes[1, 1].set_ylim(-0.05, 1.1)
axes[1, 1].grid(True, linestyle=':', alpha=0.6)
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('operasi_himpunan_fuzzy_komparasi.png', dpi=300)
plt.show()