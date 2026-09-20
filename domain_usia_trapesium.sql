-- Create Database
CREATE DATABASE IF NOT EXISTS db_logika_fuzzy;
USE db_logika_fuzzy;

-- Create Table Domain Usia Trapesium
CREATE TABLE IF NOT EXISTS domain_usia (
    id_kategori INT PRIMARY KEY AUTO_INCREMENT,
    nama_kategori VARCHAR(50) NOT NULL,
    rentang_usia VARCHAR(30) NOT NULL,
    titik_a FLOAT NOT NULL,
    titik_b FLOAT NOT NULL,
    titik_c FLOAT NOT NULL,
    titik_d FLOAT NOT NULL,
    bentuk_kurva VARCHAR(20) DEFAULT 'Trapezoidal'
);

-- Insert Data Kategori Usia berdasarkan Tugas 1
INSERT INTO domain_usia (nama_kategori, rentang_usia, titik_a, titik_b, titik_c, titik_d, bentuk_kurva) VALUES
('Bayi / Anak Usia Dini', '0 - 5 tahun', 0, 0, 3, 6, 'Trapezoidal'),
('Anak-anak', '6 - 11 tahun', 4, 6, 10, 12, 'Trapezoidal'),
('Remaja', '10 - 19 tahun', 9, 11, 17, 20, 'Trapezoidal'),
('Pemuda', '15 - 24 tahun', 14, 16, 22, 25, 'Trapezoidal'),
('Dewasa', '20 - 65 tahun', 19, 23, 58, 63, 'Trapezoidal'),
('Lanjut Usia', '60 - 80+ tahun', 58, 65, 80, 80, 'Trapezoidal');

-- Query Verifikasi Data
SELECT * FROM domain_usia;