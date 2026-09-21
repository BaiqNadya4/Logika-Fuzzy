-- 1. BUAT DATABASE BARU
CREATE DATABASE db_fuzzy_usia;

-- 2. GUNAKAN DATABASE
USE db_fuzzy_usia;

-- ===================================================
-- 3. TABEL & DATA DOMAIN USIA BAYI (0-5 Tahun)
-- ===================================================
CREATE TABLE tb_domain_usia_bayi (
    id INT AUTO_INCREMENT PRIMARY KEY,
    b_bawah DECIMAL(5,2),
    b_atas DECIMAL(5,2),
    fungsi VARCHAR(50)
);

INSERT INTO tb_domain_usia_bayi (b_bawah, b_atas, fungsi) VALUES
(0.00, 0.00, '0'),
(0.00, 0.00, 'trapesium_up_bayi'),
(0.00, 3.00, '1'),
(3.00, 5.00, 'trapesium_down_bayi'),
(5.00, 150.00, '0');


-- ===================================================
-- 4. TABEL & DATA DOMAIN USIA ANAK (6-11 Tahun)
-- ===================================================
CREATE TABLE tb_domain_usia_anak (
    id INT AUTO_INCREMENT PRIMARY KEY,
    b_bawah DECIMAL(5,2),
    b_atas DECIMAL(5,2),
    fungsi VARCHAR(50)
);

INSERT INTO tb_domain_usia_anak (b_bawah, b_atas, fungsi) VALUES
(0.00, 4.00, '0'),
(4.00, 6.00, 'trapesium_up_anak'),
(6.00, 9.00, '1'),
(9.00, 11.00, 'trapesium_down_anak'),
(11.00, 150.00, '0');


-- ===================================================
-- 5. TABEL & DATA DOMAIN USIA REMAJA (10-19 Tahun)
-- ===================================================
CREATE TABLE tb_domain_usia_remaja (
    id INT AUTO_INCREMENT PRIMARY KEY,
    b_bawah DECIMAL(5,2),
    b_atas DECIMAL(5,2),
    fungsi VARCHAR(50)
);

INSERT INTO tb_domain_usia_remaja (b_bawah, b_atas, fungsi) VALUES
(0.00, 10.00, '0'),
(10.00, 12.00, 'trapesium_up_remaja'),
(12.00, 17.00, '1'),
(17.00, 19.00, 'trapesium_down_remaja'),
(19.00, 150.00, '0');


-- ===================================================
-- 6. TABEL & DATA DOMAIN USIA PEMUDA (15-24 Tahun)
-- ===================================================
CREATE TABLE tb_domain_usia_pemuda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    b_bawah DECIMAL(5,2),
    b_atas DECIMAL(5,2),
    fungsi VARCHAR(50)
);

INSERT INTO tb_domain_usia_pemuda (b_bawah, b_atas, fungsi) VALUES
(0.00, 15.00, '0'),
(15.00, 17.00, 'trapesium_up_pemuda'),
(17.00, 22.00, '1'),
(22.00, 24.00, 'trapesium_down_pemuda'),
(24.00, 150.00, '0');


-- ===================================================
-- 7. TABEL & DATA DOMAIN USIA DEWASA (20-65 Tahun)
-- ===================================================
CREATE TABLE tb_domain_usia_dewasa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    b_bawah DECIMAL(5,2),
    b_atas DECIMAL(5,2),
    fungsi VARCHAR(50)
);

INSERT INTO tb_domain_usia_dewasa (b_bawah, b_atas, fungsi) VALUES
(0.00, 20.00, '0'),
(20.00, 25.00, 'trapesium_up_dewasa'),
(25.00, 60.00, '1'),
(60.00, 65.00, 'trapesium_down_dewasa'),
(65.00, 150.00, '0');


-- ===================================================
-- 8. TABEL & DATA DOMAIN USIA LANSIA (>=65 Tahun)
-- ===================================================
CREATE TABLE tb_domain_usia_lansia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    b_bawah DECIMAL(5,2),
    b_atas DECIMAL(5,2),
    fungsi VARCHAR(50)
);

INSERT INTO tb_domain_usia_lansia (b_bawah, b_atas, fungsi) VALUES
(0.00, 60.00, '0'),
(60.00, 65.00, 'trapesium_up_lansia'),
(65.00, 150.00, '1'),
(150.00, 150.00, 'trapesium_down_lansia'),
(150.00, 150.00, '0');

SELECT * FROM tb_domain_usia_bayi;
SELECT * FROM tb_domain_usia_anak;
SELECT * FROM tb_domain_usia_remaja;
SELECT * FROM tb_domain_usia_pemuda;
SELECT * FROM tb_domain_usia_dewasa;
SELECT * FROM tb_domain_usia_lansia;