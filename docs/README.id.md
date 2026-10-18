# OriginEcho

**Pulihkan riwayat pemotretan yang hilang setelah pengeditan foto dengan AI.**

Saat Anda memotret melalui generator atau editor AI, berkas hasilnya biasanya
**telanjang**: merek dan model kamera, tanggal dan waktu pengambilan, koordinat
GPS, ISO, eksposur, dan data objektif semuanya hilang. Gambarnya tampak sama,
tetapi ceritanya hilang.

**OriginEcho** mengembalikan cerita itu. Program ini menyalin seluruh metadata
foto asli ke gambar yang telah diedit AI dan, bila dikehendaki, memulihkan
format berkas serta memberi nama baru pada hasilnya.

---

## Apa yang dilakukan

| | |
|---|---|
| **Menyalin EXIF** | kamera, model, tanggal/waktu, GPS, ISO, eksposur, objektif, panjang fokus… |
| **Menyalin XMP + IPTC** | keterangan, penulis, kata kunci, penilaian, riwayat penyuntingan |
| **Menyalin profil warna** | profil ICC, agar warna tetap presisi |
| **Memulihkan format** | hasil AI dikonversi ke format asli (PNG → JPEG, WEBP → JPEG…) |
| **Memberi nama hasil** | `nama-asli nama-edited.ext` |
| **Memulihkan tanggal berkas** | tanggal dibuat dan diubah sesuai aslinya |

## Mengapa

Alat AI membangun ulang berkas dari nol dan tidak mengetahui metadata aslinya.
OriginEcho membacanya dari asli yang belum tersentuh lalu menempelkannya ke
salinan yang telah diedit, sehingga foto akhir tetap menyimpan asalnya.

## Mulai cepat

1. Klik ganda **`OriginEcho.bat`** (Windows) — jendela program terbuka.
2. Pada **ASLI**, pilih foto yang belum tersentuh (atau folder asli).
3. Pada **FOTO HASIL EDIT**, pilih hasil AI (satu berkas, beberapa berkas, atau
   folder). Anda juga bisa **menyeret dan melepaskan** berkas langsung ke kolom.
4. Klik **MULAI SALIN**.

Hasilnya muncul di samping berkas yang diedit, bernama
`<nama asli> <nama diedit>.<ekstensi asli>`.

### Opsi

- **Format seperti asli** — konversi ke format asli.
- **Nama: asli + salinan** — beri nama «asli + spasi + salinan».
- **Hapus berkas lama** — hapus salinan sebelum diganti nama.
- **Salin tanggal berkas** — terapkan tanggal buat/ubah.

## Baris perintah

```bash
python tools/copy_photo_metadata.py asli.jpg diedit.jpg [lagi.jpg ...]
python tools/copy_photo_metadata.py --folder FOLDER_ASLI FOLDER_DIEDIT
```

Bendera: `--no-icc`, `--no-dates`, `--no-convert`, `--no-rename`, `--keep-old`.

## Bahasa yang didukung

Antarmuka tersedia dalam **11 bahasa** — pilih di sudut kanan atas; pilihan Anda
diingat:

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## Format berkas

Masuk/keluar: **JPEG, PNG, WEBP, TIFF**. HEIC didukung bila `pillow-heif`
terpasang.

## Catatan & kualitas

- Untuk **JPEG → JPEG**, OriginEcho menyunting berkas pada tingkat byte, sehingga
  data gambar dipertahankan **tanpa kehilangan** — tanpa kompresi ulang.
- Konversi antarformat (mis. PNG → JPEG) tentu mengodekan ulang gambar.
- PNG/WEBP transparan diratakan di atas latar putih saat diubah ke JPEG.
- PNG dan WEBP hanya mendukung sebagian bidang EXIF (batasan format). Untuk
  menyimpan semuanya, lebih baik gunakan JPEG.
- Penyalinan penuh (XMP/IPTC) dilakukan oleh **exiftool** (di `tools/exiftool`);
  tanpanya program hanya menangani EXIF + ICC.

## Persyaratan

- Python 3.11+
- Pillow (terpasang otomatis jika belum ada)
- `tkinterdnd2` — seret dan lepas (opsional)
- exiftool — XMP/IPTC lengkap (opsional, disertakan)

## Penghargaan

- **exiftool** karya Phil Harvey — standar emas untuk metadata gambar.
- **Pillow** — dekode/enkode gambar.
- **tkinterdnd2** — dukungan seret-lepas untuk Tkinter.

## Lisensi

MIT — bebas dipakai dan dimodifikasi.

---

<p align="center"><sub>English: <a href="../README.md">EN</a> ·
<a href="README.ru.md">RU</a> · <a href="README.de.md">DE</a> ·
<a href="README.es.md">ES</a> · <a href="README.fr.md">FR</a> ·
<a href="README.it.md">IT</a> · <a href="README.tr.md">TR</a> ·
<a href="README.hi.md">HI</a> · <a href="README.ko.md">KO</a> ·
<a href="README.zh.md">ZH</a></sub></p>
