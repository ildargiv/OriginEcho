# OriginEcho

**Yapay zekâ ile fotoğraf düzenlemesinden sonra kaybolan çekim geçmişini geri yükleyin.**

Bir fotoğrafı yapay zekâ üreticisinden veya editöründen geçirdiğinizde, çıktı
genellikle **çıplak** gelir: kamera markası ve modeli, çekim tarihi ve saati,
GPS koordinatları, ISO, pozlama ve objektif bilgileri kaybolur. Fotoğraf aynı
görünür ama hikâyesi gider.

**OriginEcho** o hikâyeyi geri verir. Orijinal fotoğrafın tüm meta
verilerini yapay zekâ ile düzenlenmiş görsele kopyalar; isterseniz dosya formatını
da geri yükler ve sonucu yeniden adlandırır.

---

## Ne yapar

| | |
|---|---|
| **EXIF kopyalar** | kamera, model, tarih/saat, GPS, ISO, pozlama, objektif, odak uzaklığı… |
| **XMP + IPTC kopyalar** | açıklamalar, sanatçı, anahtar kelimeler, puan, düzenleme geçmişi |
| **Renk profilini kopyalar** | ICC profili, renklerin tam olarak korunması için |
| **Formatı geri yükler** | YZ çıktısı orijinalin formatına dönüştürülür (PNG → JPEG, WEBP → JPEG…) |
| **Sonucu yeniden adlandırır** | `orijinal-ad düzenlenmiş-ad.uz` |
| **Dosya tarihlerini geri yükler** | oluşturma/değiştirme tarihleri orijinalle aynı olur |

## Neden

YZ araçları dosyayı sıfırdan yeniden üretir ve orijinalin meta verilerini
bilmez. OriginEcho bunları dokunulmamış orijinalden okuyup düzenlenmiş kopyaya
ekler; böylece nihai fotoğraf kökenini korur.

## Hızlı başlangıç

1. **`OriginEcho.bat`** dosyasına çift tıklayın (Windows) — program penceresi açılır.
2. **ORİJİNAL** alanında dokunulmamış fotoğrafı (veya bir klasörü) seçin.
3. **DÜZENLENMİŞ FOTOĞRAFLAR** alanında YZ çıktısını seçin (bir dosya, birkaç
   dosya veya klasör). Dosyaları doğrudan alanlara **sürükleyip bırakabilirsiniz**.
4. **AKTARIMI BAŞLAT** düğmesine basın.

Sonuç, düzenlenmiş dosyanın yanında
`<orijinal ad> <düzenlenmiş ad>.<orijinal uzantısı>` adıyla oluşur.

### Seçenekler

- **Orijinal biçimde** — orijinalin biçimine dönüştür.
- **Ad: orijinal + kopya** — «orijinal + boşluk + kopya» olarak yeniden adlandır.
- **Eski dosyayı sil** — adlandırma sonrası eski kopyayı kaldır.
- **Dosya tarihlerini kopyala** — oluşturma/değiştirme tarihlerini uygula.

## Komut satırı

```bash
python tools/copy_photo_metadata.py orijinal.jpg duzenlenmis.jpg [daha fazla.jpg ...]
python tools/copy_photo_metadata.py --folder ORIJINALLER KLASORU DuzENLENMISLER
```

Bayraklar: `--no-icc`, `--no-dates`, `--no-convert`, `--no-rename`, `--keep-old`.

## Desteklenen diller

Arayüz **11 dilde** kullanılabilir — sağ üst köşeden birini seçin; seçiminiz
hatırlanır:

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## Desteklenen dosya biçimleri

Giriş/çıkış: **JPEG, PNG, WEBP, TIFF**. `pillow-heif` kuruluysa HEIC de
desteklenir.

## Notlar ve kalite

- **JPEG → JPEG** durumunda OriginEcho dosyayı bayt düzeyinde düzenler, böylece
  görüntü verileri **kayıpsız** korunur — yeniden sıkıştırma yapılmaz.
- Biçimler arası dönüştürme (örn. PNG → JPEG) görüntüyü yeniden kodlar.
- Şeffaf PNG/WEBP, JPEG’e çevrilirken beyaz zemin üzerine düzleştirilir.
- PNG ve WEBP yalnızca bazı EXIF alanlarını destekler (bu bir biçim sınırıdır).
  Tamamını korumak için JPEG tercih edin.
- Tam aktarım (XMP/IPTC) **exiftool** tarafından yapılır (`tools/exiftool`);
  yoksa program EXIF + ICC ile sınırlıdır.

## Gereksinimler

- Python 3.11+
- Pillow (yoksa otomatik kurulur)
- `tkinterdnd2` — sürükle-bırak (isteğe bağlı)
- exiftool — tam XMP/IPTC (isteğe bağlı, dahildir)

## Teşekkürler

- **exiftool**, Phil Harvey — görüntü meta verilerinde altın standart.
- **Pillow** — görüntü kodlama/körlme.
- **tkinterdnd2** — Tkinter için sürükle-bırak desteği.

## Lisans

MIT — serbestçe kullanılabilir ve değiştirilebilir.

---

<p align="center"><sub>English: <a href="../README.md">EN</a> ·
<a href="README.ru.md">RU</a> · <a href="README.de.md">DE</a> ·
<a href="README.es.md">ES</a> · <a href="README.fr.md">FR</a> ·
<a href="README.it.md">IT</a> · <a href="README.hi.md">HI</a> ·
<a href="README.id.md">ID</a> · <a href="README.ko.md">KO</a> ·
<a href="README.zh.md">ZH</a></sub></p>
