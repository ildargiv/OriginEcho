# OriginEcho

**Ripristina la cronologia dello scatto persa dopo l’editing con IA.**

Quando fai passare una fotografia da un generatore o editor IA, il file in
uscita di solito è **nudo**: marca e modello della fotocamera, data e ora dello
scatto, coordinate GPS, ISO, esposizione e dati dell’obiettivo spariscono.
L’immagine sembra uguale, ma la sua storia è andata perduta.

**OriginEcho** restituisce quella storia. Copia tutti i metadati della foto
originale sull’immagine modificata dall’IA e, a scelta, ripristina anche il
formato file e rinomina il risultato.

---

## Cosa fa

| | |
|---|---|
| **Copia EXIF** | fotocamera, modello, data/ora, GPS, ISO, esposizione, obiettivo, focale… |
| **Copia XMP + IPTC** | didascalie, autore, parole chiave, valutazione, cronologia delle modifiche |
| **Copia il profilo colore** | profilo ICC, per mantenere i colori esatti |
| **Ripristina il formato** | il risultato IA viene convertito nel formato dell’originale (PNG → JPEG, WEBP → JPEG…) |
| **Rinomina il risultato** | `nome-originale nome-modificato.ext` |
| **Ripristina le date** | date di creazione e modifica come l’originale |

## Perché

Gli strumenti IA ricostruiscono il file da zero e ignorano i metadati
dell’originale. OriginEcho li legge dall’originale intatto e li innesta nella
copia modificata, così la foto finale conserva la sua provenienza.

## Avvio rapido

1. Fai doppio clic su **`OriginEcho.bat`** (Windows) — si apre la finestra.
2. In **ORIGINALE**, scegli la foto intatta (o una cartella di originali).
3. In **FOTO MODIFICATE**, scegli il risultato dell’IA (un file, più file o una
   cartella). Puoi anche **trascinare e rilasciare** i file direttamente nei
   campi.
4. Premi **AVVIA TRASFERIMENTO**.

Il risultato compare accanto al file modificato, chiamato
`<nome originale> <nome modificato>.<estensione originale>`.

### Opzioni

- **Formato come l’originale** — converti nel formato dell’originale.
- **Nome: originale + copia** — rinomina come «originale + spazio + copia».
- **Elimina il vecchio file** — rimuovi la copia precedente alla rinomina.
- **Copia le date** — applica le date di creazione/modifica.

## Riga di comando

```bash
python tools/copy_photo_metadata.py originale.jpg modificato.jpg [altri.jpg ...]
python tools/copy_photo_metadata.py --folder CARTELLA_ORIGINALI CARTELLA_MODIFICATI
```

Opzioni: `--no-icc`, `--no-dates`, `--no-convert`, `--no-rename`, `--keep-old`.

## Lingue supportate

L’interfaccia è disponibile in **11 lingue** — scegline una nell’angolo in alto a
destra; la scelta viene ricordata:

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## Formati file supportati

Ingresso/uscita: **JPEG, PNG, WEBP, TIFF**. HEIC è supportato se è installato
`pillow-heif`.

## Note e qualità

- Per **JPEG → JPEG**, OriginEcho modifica il file a livello di byte, quindi i
  dati dell’immagine sono conservati **senza perdita di qualità** — nessuna
  ricompressione.
- La conversione tra formati (es. PNG → JPEG) comporta inevitabilmente una
  ricodifica.
- I PNG/WEBP trasparenti vengono appoggiati su sfondo bianco convertendoli in
  JPEG.
- PNG e WEBP supportano solo alcuni campi EXIF (limite dei formati). Per
  conservare tutto, è preferibile il JPEG.
- Il trasferimento completo (XMP/IPTC) è effettuato da **exiftool** (in
  `tools/exiftool`); senza di esso il programma si limita a EXIF + ICC.

## Requisiti

- Python 3.11+
- Pillow (installato automaticamente se mancante)
- `tkinterdnd2` — trascina e rilascia (facoltativo)
- exiftool — XMP/IPTC completo (facoltativo, incluso)

## Crediti

- **exiftool** di Phil Harvey — lo standard di riferimento per i metadati.
- **Pillow** — codifica/decodifica delle immagini.
- **tkinterdnd2** — supporto drag & drop per Tkinter.

## Licenza

MIT — libero da usare e modificare.

---

<p align="center"><sub>English: <a href="../README.md">EN</a> ·
<a href="README.ru.md">RU</a> · <a href="README.de.md">DE</a> ·
<a href="README.es.md">ES</a> · <a href="README.fr.md">FR</a> ·
<a href="README.tr.md">TR</a> · <a href="README.hi.md">HI</a> ·
<a href="README.id.md">ID</a> · <a href="README.ko.md">KO</a> ·
<a href="README.zh.md">ZH</a></sub></p>
