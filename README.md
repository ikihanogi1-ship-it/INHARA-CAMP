# INHARA CAMP

Aplikasi administrasi lokal untuk satu admin yang mengelola penyewaan alat camping.
Fitur meliputi data kategori dan alat, identitas penyewa, ketersediaan stok per
periode, perhitungan biaya sewa, pengembalian, denda keterlambatan, serta ekspor
riwayat transaksi ke CSV. Identitas penyewa juga dapat dikelola melalui menu
tersendiri, selain dicatat saat membuat penyewaan.

Status perlengkapan pada menu **Data alat** ditampilkan untuk setiap unit dengan
kode unik: **Tersedia**, **Akan datang**, **Sedang disewa**, **Terlambat**,
**Dikembalikan hari ini**, atau **Tidak aktif**. Riwayat transaksi menunjukkan
kode unit yang dialokasikan ke penyewa. Menu **Transaksi** dan **Pengembalian**
dipisahkan, dan masing-masing menampilkan stok total, jumlah sedang disewa,
serta sisa stok tersedia untuk setiap jenis alat.
Menu **Kategori alat** dan **Data alat** tersedia langsung di navigasi bawah logo,
sehingga pengelolaan kategori tidak tersembunyi di dalam tab inventaris.
Menu **Identitas penyewa** menyediakan tambah, lihat, ubah, dan hapus data
penyewa. Detail perlengkapan dicatat bersama transaksi penyewaan, sedangkan
tanggal aktual pengembalian dan denda dicatat melalui menu **Pengembalian**.

## Menjalankan aplikasi

Simpan `Logo Inhara.png` di folder yang sama dengan `app.py`. Logo digunakan
pada navigasi dan banner dashboard.

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Buka `http://127.0.0.1:8501`. Server hanya menerima koneksi dari komputer ini.
Data disimpan dalam `inhara_camp.db` di folder aplikasi. Aplikasi tidak memiliki
login, sesuai ruang lingkup satu admin.

Saat pertama kali dijalankan, aplikasi menambahkan kategori dan satu alat contoh
jenis Tenda bernama Tenda 4 Orang dengan tarif Rp50.000 per hari. Data
perlengkapan memiliki kolom **Jenis alat** dan **Nama alat**. Pada pengelolaan
kategori, gunakan **Jenis kategori** dan **Nama alat**. Sesuaikan data contoh
tersebut melalui menu **Data alat** sebelum dipakai untuk operasional.

Setiap unit stok memiliki kode unik, misalnya `ALT001-001`, `ALT001-002`.
Status inventaris ditampilkan per kode unit, dan kode unit yang dialokasikan
akan muncul pada rincian transaksi penyewaan.
