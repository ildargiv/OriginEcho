# OriginEcho

**Restaurer l’historique de prise de vue perdu après l’édition IA.**

Quand vous faites passer une photo dans un générateur ou un éditeur IA, le fichier
exporté sort généralement **nu** : la marque et le modèle de l’appareil, la date
et l’heure de la prise de vue, les coordonnées GPS, l’ISO, l’exposition et les
données de l’objectif ont disparu. L’image paraît identique, mais son histoire
s’est évaporée.

**OriginEcho** rend cette histoire. Il copie l’intégralité des métadonnées de la
photo d’origine sur l’image retouchée par l’IA et, en option, rétablit le format
de fichier d’origine et renomme le résultat.

---

## Ce qu’il fait

| | |
|---|---|
| **Copie l’EXIF** | appareil, modèle, date/heure, GPS, ISO, exposition, objectif, focale… |
| **Copie XMP + IPTC** | légendes, auteur, mots-clés, note, historique d’édition |
| **Copie le profil colorimétrique** | profil ICC, pour des couleurs fidèles |
| **Rétablit le format** | le résultat IA est converti au format de l’original (PNG → JPEG, WEBP → JPEG…) |
| **Renomme le résultat** | `nom-original nom-retouche.ext` |
| **Rétablit les dates** | dates de création et de modification comme l’original |

## Pourquoi

Les outils IA reconstruisent le fichier de zéro et ignorent les métadonnées de
l’original. OriginEcho les lit sur l’original intact et les greffe sur la copie
retouchée, afin que la photo finale garde sa provenance.

## Démarrage rapide

1. Double-cliquez sur **`OriginEcho.bat`** (Windows) — la fenêtre s’ouvre.
2. Dans **ORIGINALE**, choisissez la photo intacte (ou un dossier d’originaux).
3. Dans **PHOTOS RETOUCHÉES**, choisissez le résultat de l’IA (un fichier,
   plusieurs fichiers ou un dossier). Vous pouvez aussi **glisser-déposer** les
   fichiers directement dans les champs.
4. Cliquez sur **LANCER LE TRANSFERT**.

Le résultat apparaît à côté du fichier retouché, nommé
`<nom original> <nom retouché>.<extension d’origine>`.

### Options

- **Format comme l’original** — convertir au format de l’original.
- **Nom : original + copie** — renommer « original + espace + copie ».
- **Supprimer l’ancien fichier** — supprimer la copie d’après le renommage.
- **Copier les dates** — appliquer les dates de création/modification.

## Ligne de commande

```bash
python tools/copy_photo_metadata.py original.jpg retouche.jpg [plus.jpg ...]
python tools/copy_photo_metadata.py --folder DOSSIER_ORIGINAUX DOSSIER_REToucheS
```

Options : `--no-icc`, `--no-dates`, `--no-convert`, `--no-rename`, `--keep-old`.

## Agents IA (MCP)

OriginEcho peut fonctionner comme **serveur MCP** (Model Context Protocol) : les
assistants IA — Claude Desktop, OpenCode, Cursor, etc. — peuvent restaurer les
métadonnées en langage naturel.

Lancez le même `OriginEcho.exe` avec le drapeau `--mcp` (transport stdio, local
uniquement, sans port ni trafic réseau) :

```json
{
  "mcpServers": {
    "originecho": {
      "command": "C:\\Program Files\\OriginEcho\\OriginEcho.exe",
      "args": ["--mcp"]
    }
  }
}
```

Depuis les sources : `"command": "python", "args": ["C:\\chemin\\vers\\tools\\mcp_server.py"]`.

Outils disponibles :

| Outil | Rôle |
|---|---|
| `photo_info` | Lit l'historique de prise d'un fichier (appareil, date, ISO, GPS...) |
| `restore_metadata` | Copie EXIF/XMP/IPTC/ICC de l'original vers la photo retouchée |
| `process_folders` | Traite deux dossiers par lot |
| `supported_formats` | Liste les formats pris en charge |
| `app_info` | Version et vérification des composants |

Exemple : « Transfère les métadonnées de IMG_20261017_142755.jpg vers toutes les photos du dossier Edited ».

## Langues prises en charge

L’interface est disponible en **11 langues** — choisissez-en une dans le coin
supérieur droit ; le choix est mémorisé :

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## Formats de fichiers

Entrée/sortie : **JPEG, PNG, WEBP, TIFF**. HEIC est pris en charge si
`pillow-heif` est installé.

## Notes et qualité

- Pour **JPEG → JPEG**, OriginEcho modifie le fichier au niveau des octets : les
  données d’image sont conservées **sans perte** — aucune recompression.
- La conversion entre formats (p. ex. PNG → JPEG) réencode nécessairement
  l’image.
- Les PNG/WEBP transparents sont aplatis sur fond blanc lors du passage en JPEG.
- PNG et WEBP ne prennent en charge que certains champs EXIF (limite de ces
  formats). Pour tout conserver, préférez le JPEG.
- La copie complète (XMP/IPTC) est assurée par **exiftool** (dans
  `tools/exiftool`) ; sans lui, le programme se limite à EXIF + ICC.

## Prérequis

- Python 3.11+
- Pillow (installé automatiquement si absent)
- `tkinterdnd2` — glisser-déposer (facultatif)
- exiftool — XMP/IPTC complet (facultatif, fourni)

## Crédits

- **exiftool** de Phil Harvey — la référence en métadonnées d’image.
- **Pillow** — décodage/codage d’images.
- **tkinterdnd2** — glisser-déposer pour Tkinter.

## Licence

MIT — libre d’utilisation et de modification.

---

<p align="center"><sub>English: <a href="../README.md">EN</a> ·
<a href="README.ru.md">RU</a> · <a href="README.de.md">DE</a> ·
<a href="README.es.md">ES</a> · <a href="README.it.md">IT</a> ·
<a href="README.tr.md">TR</a> · <a href="README.hi.md">HI</a> ·
<a href="README.id.md">ID</a> · <a href="README.ko.md">KO</a> ·
<a href="README.zh.md">ZH</a></sub></p>
