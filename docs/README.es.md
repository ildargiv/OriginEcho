# OriginEcho

**Restaura el historial de captura perdido tras editar la foto con IA.**

Cuando pasas una fotografía por un generador o editor de IA, el archivo de salida
suele quedar **desnudo**: la marca y el modelo de la cámara, la fecha y hora de la
toma, las coordenadas GPS, el ISO, la exposición y los datos del objetivo
desaparecen. La imagen se ve igual, pero su historia se ha perdido.

**OriginEcho** devuelve esa historia. Copia todos los metadatos de la foto
original sobre la imagen editada por IA y, opcionalmente, recupera también el
formato de archivo y renombra el resultado.

---

## Qué hace

| | |
|---|---|
| **Copia EXIF** | cámara, modelo, fecha/hora, GPS, ISO, exposición, objetivo, distancia focal… |
| **Copia XMP + IPTC** | descripciones, autor, palabras clave, valoración, historial de edición |
| **Copia el perfil de color** | perfil ICC, para que los colores se mantengan exactos |
| **Restaura el formato** | el resultado de IA se convierte al formato del original (PNG → JPEG, WEBP → JPEG…) |
| **Renombra el resultado** | `nombre-original nombre-editado.ext` |
| **Restaura las fechas** | fechas de creación y modificación como en el original |

## Por qué

Las herramientas de IA reconstruyen el archivo desde cero y no conocen los
metadatos del original. OriginEcho los lee del original intacto y los injerta en
la copia editada, de modo que la foto final conserva su procedencia.

## Inicio rápido

1. Haz doble clic en **`OriginEcho.bat`** (Windows) — se abre la ventana.
2. En **ORIGINAL**, elige la foto intacta (o una carpeta de originales).
3. En **FOTOS EDITADAS**, elige la salida de IA (archivo, varios archivos o una
   carpeta). También puedes **arrastrar y soltar** archivos en los campos.
4. Pulsa **REALIZAR TRANSFERENCIA**.

El resultado aparece junto al archivo editado, con el nombre
`<nombre original> <nombre editado>.<extensión original>`.

### Opciones

- **Formato como el original** — convertir al formato del original.
- **Nombre: original + copia** — renombrar como «original + espacio + copia».
- **Eliminar archivo antiguo** — borrar la copia previa al renombrado.
- **Copiar fechas** — aplicar las fechas de creación/modificación.

## Línea de comandos

```bash
python tools/copy_photo_metadata.py original.jpg editado.jpg [mas.jpg ...]
python tools/copy_photo_metadata.py --folder CARPETA_ORIGENES CARPETA_EDITADAS
```

Opciones: `--no-icc`, `--no-dates`, `--no-convert`, `--no-rename`, `--keep-old`.

## Idiomas soportados

La interfaz está disponible en **11 idiomas** — elige uno en la esquina superior
derecha; la selección se recuerda:

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## Formatos de archivo

Entrada/salida: **JPEG, PNG, WEBP, TIFF**. HEIC se admite si está instalado
`pillow-heif`.

## Notas y calidad

- Para **JPEG → JPEG**, OriginEcho edita el archivo a nivel de bytes, por lo que
  los datos de imagen se conservan **sin pérdida** — sin recompresión.
- Convertir entre formatos (p. ej. PNG → JPEG) implica recodificar la imagen.
- Los PNG/WEBP transparentes se aplanan sobre fondo blanco al pasar a JPEG.
- PNG y WEBP admiten solo algunos campos EXIF (limitación de los formatos). Para
  conservar todo, conviene usar JPEG.
- La copia completa (XMP/IPTC) la hace **exiftool** (en `tools/exiftool`); sin él
  el programa se limita a EXIF + ICC.

## Requisitos

- Python 3.11+
- Pillow (se instala solo si falta)
- `tkinterdnd2` — arrastrar y soltar (opcional)
- exiftool — XMP/IPTC completo (opcional, incluido)

## Créditos

- **exiftool** de Phil Harvey — el estándar de oro en metadatos de imagen.
- **Pillow** — decodificación/codificación de imágenes.
- **tkinterdnd2** — arrastrar y soltar para Tkinter.

## Licencia

MIT — libre para usar y modificar.

---

<p align="center"><sub>English: <a href="../README.md">EN</a> ·
<a href="README.ru.md">RU</a> · <a href="README.de.md">DE</a> ·
<a href="README.fr.md">FR</a> · <a href="README.it.md">IT</a> ·
<a href="README.tr.md">TR</a> · <a href="README.hi.md">HI</a> ·
<a href="README.id.md">ID</a> · <a href="README.ko.md">KO</a> ·
<a href="README.zh.md">ZH</a></sub></p>
