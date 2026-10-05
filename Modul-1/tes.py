def fuzzifikasi_usia(x):

    cursor = db.cursor()

    query = """
        SELECT usia_min, usia_max, nilai_fuzzy
        FROM usia_remaja
        WHERE %s >= usia_min
        AND %s <= usia_max
    """

    cursor.execute(query, (x, x))

    data = cursor.fetchone()

    cursor.close()

    if data is None:
        return None

    usia_min, usia_max, nama_fungsi = data

    if nama_fungsi == "0":
        return 0

    if nama_fungsi in fungsi:

        fungsi_y = fungsi[nama_fungsi]

        nilai = fungsi_y(x)

        return nilai

    raise ValueError(
        f"Fungsi '{nama_fungsi}' belum dibuat di Python."
    )