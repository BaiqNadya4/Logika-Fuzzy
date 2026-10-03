# Praktikum 1 — Pengantar Logika Fuzzy dan Representasi Derajat Keanggotaan
## Konsep Ketidakpastian, Logika Crisp vs Fuzzy, dan Visualisasi Derajat Keanggotaan dengan Python

---

## A. Tujuan Praktikum
Setelah menyelesaikan praktikum ini, mahasiswa diharapkan mampu:
1. Menjelaskan konsep ketidakpastian dalam pengambilan keputusan di bidang Teknologi Informasi.
2. Membedakan secara matematis dan konseptual antara logika Boolean (crisp) dan logika fuzzy.
3. Menjelaskan arti nilai derajat keanggotaan $\mu(x) \in [0, 1]$ dan membedakannya dari konsep probabilitas.
4. Mengimplementasikan fungsi karakteristik crisp dan fungsi keanggotaan fuzzy menggunakan bahasa pemrograman Python.
5. Memvisualisasikan perbandingan logika crisp dan fuzzy menggunakan pustaka `NumPy` dan `Matplotlib`.
6. Menganalisis perilaku sistem pada kondisi batas (*boundary conditions*) dan menjelaskan keunggulan transisi halus (*smooth transition*) pada logika fuzzy.

> [!NOTE]
> **Prasyarat Pengetahuan:** Dasar pemrograman Python (variabel, fungsi, percabangan), dasar array numerik, dan konsep himpunan matematika dasar.

---

## B. Konsep Dasar

### 1. Masalah Pengambilan Keputusan dalam Kondisi Ketidakpastian
Dalam dunia nyata, khususnya pada bidang Teknologi Informasi, parameter sistem sering kali tidak dapat dikelompokkan secara kaku (*black-and-white*). Perhatikan contoh permasalahan berikut:
- **Waktu Respons Server (*Response Time*):** Apakah waktu respons 3.9 detik dikategorikan *Cepat* atau *Lambat* jika ambang batas kaku ditetapkan pada 4.0 detik?
- **Suhu Ruang Server (*Data Center Temperature*):** Jika batas dingin adalah
  $$\le 20^\circ\text{C}$$
  , apakah
  $$20.1^\circ\text{C}$$
  otomatis dianggap *Panas*?
- **Kualitas Layanan (*Quality of Service - QoS*):** Penilaian pengguna mengenai antarmuka aplikasi sering kali dinyatakan dengan ungkapan linguistik: *"sangat memuaskan"*, *"cukup baik"*, atau *"agak lambat"*.

Pendekatan konvensional menggunakan **Logika Crisp (Boolean)** yang hanya mengenal dua keadaan diskrit:
$$\text{Nilai Keanggotaan} \in \{0, 1\} \quad (\text{SALAH / BENAR})$$


Sebaliknya, **Logika Fuzzy**, yang diperkenalkan oleh **Prof. Lotfi A. Zadeh pada tahun 1965** di University of California, Berkeley, memperluas konsep tersebut sehingga suatu nilai dapat memiliki keanggotaan bertingkat:
$$\text{Derajat Keanggotaan } \mu_A(x) \in [0, 1]$$

```text
Logika Crisp (Tegas)            Logika Fuzzy (Samar / Fleksibel)
Derajat                          Derajat
  1.0 ──────┐                      1.0 ──────┐
            │                                │\
            │                                │ \
            │                                │  \
  0.0 ──────┴───────               0.0 ──────┴───\──────
            Ambang                           Transisi Halus
```

### 2. Perbedaan Logika Crisp dan Logika Fuzzy

| Karakteristik | Logika Crisp / Boolean | Logika Fuzzy |
|---|---|---|
| **Rentang Nilai** | Biner: $\{0, 1\}$ | Kontinu: $[0.0, 1.0]$ |
| **Batas Himpunan** | Kaku, terputus (*crisp boundary*) | Halus, bertahap (*gradual transition*) |
| **Representasi Makna** | Hanya YA atau TIDAK | Sebagian benar, agak benar, sangat benar |
| **Ketahanan Noise** | Rentan terhadap fluktuasi kecil di sekitar ambang | Stabil dan toleran terhadap variasi data input |
| **Representasi Komputasi** | `bool` / `int` (0 atau 1) | `float` ($0.0 \le x \le 1.0$) |

### 3. Derajat Keanggotaan vs Probabilitas
Sering terjadi kesalahpahaman antara derajat keanggotaan fuzzy dan teori probabilitas:
- **Probabilitas** mengukur *kemungkinan terjadinya suatu peristiwa acak di masa depan*, dengan syarat total peluang semesta peristiwa adalah 1 ($\sum P = 1$).
- **Derajat Keanggotaan Fuzzy ($\mu$)** mengukur *tingkat kesesuaian data terhadap suatu konsep linguistik yang sudah terjadi*. Derajat keanggotaan tidak mensyaratkan jumlah total bernilai 1.

---

## C. Formulasi Matematis

### 1. Fungsi Karakteristik Himpunan Crisp
Misalkan semesta pembicaraan adalah $X$. Suatu himpunan crisp $A$ didefinisikan oleh fungsi karakteristik $\chi_A(x)$:

$$
\chi_A(x) =
\begin{cases}
1, & \text{jika } x \in A \\
0, & \text{jika } x \notin A 
\end{cases}
$$

Contoh untuk penilaian *Layanan Memuaskan* dengan skala rating $1 \le x \le 5$ dan batas ambang $\theta = 4.0$:

$$
\chi_{\text{Memuaskan}}(x) = 
\begin{cases} 
1, & x \ge 4.0 \\ 
0, & x < 4.0 
\end{cases}
$$

### 2. Fungsi Keanggotaan Himpunan Fuzzy
Pada himpunan fuzzy $A$, setiap elemen $x$ dipetakan ke dalam interval real $[0, 1]$ oleh fungsi keanggotaan $\mu_A(x)$:

$$\mu_A(x): X \to [0, 1]$$

Contoh model linear naik untuk konsep *Layanan Memuaskan* pada domain $[2.5, 4.5]$:

$$
\mu_{\text{Memuaskan}}(x) = 
\begin{cases} 
0, & x < 2.5 \\ 
\dfrac{x - 2.5}{4.5 - 2.5} = 
\dfrac{x - 2.5}{2.0}, & 2.5 \le x \le 4.5 \\ 
1, & x > 4.5 
\end{cases}
$$

---

## D. Implementasi dalam Python

### 1. Persiapan Lingkungan
Pastikan pustaka `numpy` dan `matplotlib` sudah terpasang. Jalankan di terminal jika belum:
```bash
pip install numpy matplotlib
```

### 2. Kode Program Perbandingan Crisp vs Fuzzy
Buat file bernama `pertemuan1_crisp_vs_fuzzy.py` atau jalankan pada Jupyter Notebook:

```python
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# 1. DEFINISI FUNGSI KARAKTERISTIK CRISP
# ==========================================================
def crisp_memuaskan(rating, threshold=4.0):
    """
    Fungsi karakteristik crisp.
    Mengembalikan 1 jika rating >= threshold, selain itu 0.
    """
    return np.where(rating >= threshold, 1.0, 0.0)


# ==========================================================
# 2. DEFINISI FUNGSI KEANGGOTAAN FUZZY
# ==========================================================
def fuzzy_memuaskan(rating, a=2.5, b=4.5):
    """
    Fungsi keanggotaan fuzzy linear naik.
    - x <= a       : derajat 0
    - a <= x <= b  : derajat (x - a) / (b - a)
    - x >= b       : derajat 1
    """
    derajat = (rating - a) / (b - a)
    return np.clip(derajat, 0.0, 1.0)


# ==========================================================
# 3. GENERASI DATA SEMESTA PEMBICARAAN
# ==========================================================
# Domain rating layanan dari 1.0 sampai 5.0
ratings = np.linspace(1.0, 5.0, 500)

y_crisp = crisp_memuaskan(ratings, threshold=4.0)
y_fuzzy = fuzzy_memuaskan(ratings, a=2.5, b=4.5)


# ==========================================================
# 4. VISUALISASI PERBANDINGAN
# ==========================================================
plt.figure(figsize=(10, 5))

# Plot Logika Crisp
plt.step(ratings, y_crisp, label='Crisp (Threshold = 4.0)', 
         color='#d9534f', linewidth=2.5, where='post')

# Plot Logika Fuzzy
plt.plot(ratings, y_fuzzy, label='Fuzzy (Linear Naik [2.5, 4.5])', 
         color='#0275d8', linewidth=2.5)

# Penanda titik batas kritis
plt.axvline(x=3.9, color='gray', linestyle='--', alpha=0.7)
plt.axvline(x=4.0, color='gray', linestyle='--', alpha=0.7)
plt.scatter([3.9, 4.0], [crisp_memuaskan(3.9), crisp_memuaskan(4.0)], 
            color='#d9534f', zorder=5, s=60)
plt.scatter([3.9, 4.0], [fuzzy_memuaskan(3.9), fuzzy_memuaskan(4.0)], 
            color='#0275d8', zorder=5, s=60)

plt.title('Perbandingan Logika Crisp vs Logika Fuzzy: Kategori "Layanan Memuaskan"', fontsize=13, fontweight='bold')
plt.xlabel('Rating Pengguna (Skala 1 - 5)', fontsize=11)
plt.ylabel('Derajat Keanggotaan / Nilai Kebenaran', fontsize=11)
plt.ylim(-0.05, 1.1)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()

# Simpan dan tampilkan grafik
plt.savefig('visualisasi_crisp_vs_fuzzy.png', dpi=300)
plt.show()
```

---

## E. Analisis Kondisi Batas (*Boundary Sensitivity*)

Mari amati output program untuk dua nilai rating yang sangat berdekatan di sekitar ambang batas $4.0$:

```python
test_values = [3.8, 3.9, 3.99, 4.0, 4.01, 4.2]

print(f"{'Rating':<8} | {'Crisp':<8} | {'Fuzzy mu(x)':<12} | {'Interpretasi Fuzzy'}")
print("-" * 55)
for val in test_values:
    c_val = float(crisp_memuaskan(val))
    f_val = float(fuzzy_memuaskan(val))
    interpretasi = f"Tingkat pemenuhan {f_val*100:.1f}%"
    print(f"{val:<8.2f} | {c_val:<8.1f} | {f_val:<12.3f} | {interpretasi}")
```

### Hasil Eksekusi:
```text
Rating   | Crisp    | Fuzzy mu(x)  | Interpretasi Fuzzy
-------------------------------------------------------
3.80     | 0.0      | 0.650        | Tingkat pemenuhan 65.0%
3.90     | 0.0      | 0.700        | Tingkat pemenuhan 70.0%
3.99     | 0.0      | 0.745        | Tingkat pemenuhan 74.5%
4.00     | 1.0      | 0.750        | Tingkat pemenuhan 75.0%
4.01     | 1.0      | 0.755        | Tingkat pemenuhan 75.5%
4.20     | 1.0      | 0.850        | Tingkat pemenuhan 85.0%
```

> [!WARNING]
> **Kelemahan Logika Crisp:**
> Perubahan sekecil $0.01$ dari $3.99$ ke $4.00$ menyebabkan perubahan ekstrem dari $0.0$ (Ditolak / Tidak Memuaskan) menjadi $1.0$ (Diterima / Memuaskan). Pada sistem penilaian beasiswa, penentuan tiket prioritas, atau alarm kebakaran, kondisi ini memicu anomali keputusan diskriminatif pada data di sekitar batas ambang.

---

## F. Praktikum Mandiri di Laboratorium

Ikuti langkah-langkah berikut:
1. Buka VS Code / Jupyter Lab dan buat file script Python baru.
2. Ketik dan jalankan program visualisasi di atas.
3. Modifikasi fungsi keanggotaan fuzzy agar menggunakan bentuk **Sigmoid** sederhana:
   $$\mu(x) = \frac{1}{1 + e^{-k(x - x_0)}}$$
   di mana $x_0$ adalah titik tengah (misal $3.5$) dan $k$ adalah kecuraman lereng (misal $2.0$).
4. Gambarkan grafik kurva Sigmoid tersebut berdampingan dengan kurva linear naik dan kurva crisp.

---

## G. Tugas Praktikum 1

### Kasus: Sistem Prioritas Tiket Helpdesk TI
Departemen Dukungan TI mengelompokkan waktu tunggu penyelesaian tiket (dalam satuan jam, semesta pembicaraan $0 \le x \le 24$ jam) ke dalam kategori **"Kritis / Butuh Eskalasi Cepat"**.

1. **Rancang Logika Crisp:**
   - Tetapkan batas kaku waktu tunggu $\ge 8$ jam sebagai tiket kritis.
2. **Rancang Logika Fuzzy:**
   - Tentukan interval transisi, misalnya:
     - Waktu $< 4$ jam: derajat kritis $= 0$
     - $4 \le x \le 12$ jam: derajat kritis naik secara linear
     - Waktu $> 12$ jam: derajat kritis $= 1$
   - Turunkan persamaan matematikanya secara manual.
3. **Implementasikan dalam Python:**
   - Buat fungsi Python untuk menghitung kedua representasi.
   - Lakukan pengujian untuk data: $2, 4, 6, 7.9, 8.0, 8.1, 10, 12, 16, 24$ jam.
   - Buat tabel perbandingannya.
4. **Visualisasikan:**
   - Simpan grafik komparasi dalam format PNG.

---

## H. Pertanyaan Analisis

Jawab pertanyaan-pertanyaan berikut secara analitis dan sertakan dalam laporan praktikum Anda:

1. Jelaskan mengapa pendekatan logika crisp dinilai kurang adil jika diterapkan pada sistem penilaian kinerja dosen atau penentuan penerima bantuan sosial!
2. Jika suatu nilai suhu memiliki derajat keanggotaan $\mu_{\text{Panas}} = 0.7$ dan $\mu_{\text{Hangat}} = 0.4$, apakah hal ini melanggar kaidah probabilitas? Jelaskan perbedaannya!
3. Pada kondisi lingkungan nyata yang penuh derau (*noisy sensors*), mengapa logika fuzzy menghasilkan keputusan yang jauh lebih stabil dibandingkan percabangan `if-else` konvensional?
4. Jelaskan apa yang dimaksud dengan semesta pembicaraan (*universe of discourse*) dan sebutkan contohnya pada sistem monitoring lalu lintas jaringan komputer!

---

## I. Ketentuan Pengumpulan
1. Mahasiswa mengunggah source code Python (`.py` atau `.ipynb`) beserta hasil grafik visualisasi ke repositori GitHub masing-masing.
2. Format penamaan file: `Modul-1/Praktikum1_<NIM>_<Nama>.ipynb` atau `.py`.
3. Commit pesan git harus deskriptif, contoh: `feat(modul1): selesaikan tugas praktikum 1 crisp vs fuzzy`.

---

## J. Kesimpulan
Pada praktikum pertama ini, Anda telah mempelajari bahwa logika fuzzy bukan pengganti logika biner, melainkan superset yang memungkinkan komputasi dengan bahasa manusia (*computing with words*). Transisi bertahap pada derajat keanggotaan $[0, 1]$ menjadi fondasi penting untuk merancang sistem pendukung keputusan yang luwes dan andal terhadap ketidakpastian informasi.
