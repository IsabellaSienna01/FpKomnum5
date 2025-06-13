import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# f(x), editable
def fungsi(x):
    return np.exp(-x**2)

# integral numerik dengan metode trapesium
def metode_trapesium(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    hasil = h / 2 * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return hasil

# integral numerik dengan metode Romberg
def integrasi_romberg(f, a, b, maks_iterasi=4):
    tabel_romberg = np.zeros((maks_iterasi, maks_iterasi))
    print("### Mengisi Kolom Pertama (Hasil Metode Trapesium) ###")
    for i in range(maks_iterasi):
        n = 2**i
        hasil_trapesium = metode_trapesium(f, a, b, n)
        tabel_romberg[i, 0] = hasil_trapesium
        print(f"Iterasi {i+1} [n={n}]: {hasil_trapesium:.8f}")
    for j in range(1, maks_iterasi):
        for i in range(j, maks_iterasi):
            ekstrapolasi = (4**j * tabel_romberg[i, j - 1] - tabel_romberg[i - 1, j - 1]) / (4**j - 1)
            tabel_romberg[i, j] = ekstrapolasi
    return tabel_romberg

# gambar graph
def gambar_graph(a, b, step, offset):
    xint = np.arange(a-offset, b+offset, 0.01)
    xtrap = np.linspace(a, b, step)
    yint = fungsi(xint)
    ytrap = fungsi(xtrap)
    plt.plot(xint, yint)
    plt.plot(xtrap, ytrap)
    plt.fill_between(xint, yint, 0, where=((xint>=a) & (xint<=b)), color="#00FF00", alpha=0.3)
    plt.fill_between(xtrap, ytrap, 0, where=((xtrap>=a) & (xtrap<=b)), color="#0000FF", alpha=0.2)
    for xi, yi in zip(xtrap, ytrap):
        plt.vlines(xi, 0, yi, colors='black', linestyles='dotted', alpha=0.7)
    plt.title('Grafik Integrasi f(x)', fontsize=16)
    plt.xlabel('x', fontsize=12)
    plt.ylabel('f(x)', fontsize=12)
    plt.show()


# contoh penggunaan, editable
batas_bawah = 0
batas_atas = 1
iterasi = 4 # n = 1, 2, 4, 8
nilai_sebenarnya = 0.74682413 # isi jika diketahui

print(">>> Memulai Perhitungan Integrasi Romberg <<<\n")
tabel_hasil = integrasi_romberg(fungsi, batas_bawah, batas_atas, iterasi)

# output tabel integrasi Romberg dengan library tabulate
print("\n### Tabel Integrasi Romberg Lengkap ###")
kolom_nama = ["Trapesium"]
for i in range(iterasi - 1):
    kolom_nama.append(f"Ekstrapolasi {i+1}")
tabel_dalam_list = [[f"{val:.8f}" if val != 0 else "0" for val in row] for row in tabel_hasil]
daftar_n = [f"n={2**i}" for i in range(iterasi)]
print(tabulate(tabel_dalam_list, headers=kolom_nama, showindex=daftar_n, tablefmt="grid", floatfmt=".8f"))

hasil_trapesium_terbaik = tabel_hasil[-1, 0]
hasil_romberg_terbaik = tabel_hasil[-1, -1]

error_trapesium = abs(hasil_trapesium_terbaik - nilai_sebenarnya)
error_romberg = abs(hasil_romberg_terbaik - nilai_sebenarnya)

# perbandingan hasil
print("\n### Perbandingan Akurasi ###")
print(f"Nilai Sebenarnya\t\t: {nilai_sebenarnya:.8f}")
print(f"Hasil Trapesium\t[n=8]\t\t: {hasil_trapesium_terbaik:.8f} (Error: {error_trapesium:.8e})")
print(f"Hasil Romberg\t[paling akurat]\t: {hasil_romberg_terbaik:.8f} (Error: {error_romberg:.8e})")

# kesimpulan
print("\n Kesimpulan : \nMetode Romberg, teknik integrasi numerik, umumnya lebih unggul daripada aturan\ntrapesium dasar karena memanfaatkan ekstrapolasi Richardson untuk mengurangi\n'true error' dan mencapai akurasi yang lebih tinggi.")

# graph
gambar_graph(batas_bawah, batas_atas, 2**(iterasi-1)+1, 0.25)
