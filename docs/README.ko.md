# OriginEcho

**AI로 사진을 편집한 뒤 사라진 촬영 기록을 되살립니다.**

사진을 AI 생성기나 편집기에 통과시키면 결과 파일은 보통 **맨손** 상태로
나옵니다. 카메라 메이커와 모델, 촬영 날짜와 시간, GPS 좌표, ISO, 노출, 렌즈
정보가 모두 지워집니다. 사진은 그대로처럼 보이지만 이야기는 사라집니다.

**OriginEcho**는 그 이야기를 되돌려줍니다. 원본 사진의 모든 메타데이터를 AI로
편집된 이미지에 복사하고, 원한다면 파일 형식까지 복원하고 결과물의 이름도 바꿔
줍니다.

---

## 무엇을 하나요

| | |
|---|---|
| **EXIF 복사** | 카메라, 모델, 날짜/시간, GPS, ISO, 노출, 렌즈, 초점 거리… |
| **XMP + IPTC 복사** | 설명, 작성자, 키워드, 평가, 편집 이력 |
| **색상 프로필 복사** | ICC 프로필로 색을 정확히 유지 |
| **형식 복원** | AI 결과를 원본 형식으로 변환 (PNG → JPEG, WEBP → JPEG…) |
| **이름 변경** | `원본이름 편집이름.확장자` |
| **파일 날짜 복원** | 생성/수정 시각을 원본과 동일하게 |

## 왜 필요한가

AI 도구는 파일을 처음부터 다시 만들기 때문에 원본의 메타데이터를 모릅니다.
OriginEcho는 손대지 않은 원본에서 이를 읽어 편집된 사본에 붙여주므로, 완성된
사진이 자신의 출처를 그대로 간직합니다.

## 빠른 시작

1. **`OriginEcho.bat`** 더블클릭 (Windows) — 프로그램 창이 열립니다.
2. **원본**에서 손대지 않은 사진(또는 원본 폴더)을 고릅니다.
3. **편집된 사진**에서 AI 결과(파일 하나, 여러 파일, 폴더)를 고릅니다. 파일을
   칸에 **직접 끌어다 놓아도** 됩니다.
4. **옮기기 실행**을 누릅니다.

결과는 편집된 파일 옆에
`<원본 이름> <편집 이름>.<원본 확장자>` 이름으로 만들어집니다.

### 옵션

- **원본과 같은 형식** — 원본 형식으로 변환.
- **이름: 원본 + 사본** — «원본 + 공백 + 사본»으로 이름 변경.
- **기존 파일 삭제** — 이름 변경 후 이전 사본 제거.
- **파일 날짜 복사** — 생성/수정 날짜 적용.

## 명령줄

```bash
python tools/copy_photo_metadata.py original.jpg edited.jpg [more.jpg ...]
python tools/copy_photo_metadata.py --folder ORIGINALS EDITED_FOLDER
```

플래그: `--no-icc`, `--no-dates`, `--no-convert`, `--no-rename`, `--keep-old`.

## 지원 언어

인터페이스는 **11개 언어**로 제공됩니다 — 오른쪽 위에서 선택하세요. 선택은
기억됩니다.

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## 지원 파일 형식

입력/출력: **JPEG, PNG, WEBP, TIFF**. `pillow-heif`가 설치되어 있으면 HEIC도
지원합니다.

## 참고 및 품질

- **JPEG → JPEG**인 경우 OriginEcho는 파일을 바이트 단위로 편집하므로 이미지
  데이터가 **손실 없이** 보존됩니다 — 재압축 없음.
- 형식 간 변환(예: PNG → JPEG)은 이미지를 다시 인코딩합니다.
- 투명 PNG/WEBP는 JPEG로 바꿀 때 흰 배경 위에 올려집니다.
- PNG와 WEBP는 일부 EXIF 필드만 지원합니다(형식의 한계). 모두 보존하려면 JPEG가
  좋습니다.
- 전체(XMP/IPTC) 복사는 **exiftool**이 수행합니다(`tools/exiftool`); 없으면
  EXIF + ICC까지만 처리합니다.

## 요구 사항

- Python 3.11+
- Pillow (없으면 자동으로 설치)
- `tkinterdnd2` — 드래그 앤 드롭(선택)
- exiftool — 전체 XMP/IPTC(선택, 포함됨)

## 감사의 말

- **exiftool**, Phil Harvey — 이미지 메타데이터의 골드 스탠다드.
- **Pillow** — 이미지 인코딩/디코딩.
- **tkinterdnd2** — Tkinter용 드래그 앤 드롭.

## 라이선스

MIT — 자유롭게 사용하고 수정할 수 있습니다.

---

<p align="center"><sub>English: <a href="../README.md">EN</a> ·
<a href="README.ru.md">RU</a> · <a href="README.de.md">DE</a> ·
<a href="README.es.md">ES</a> · <a href="README.fr.md">FR</a> ·
<a href="README.it.md">IT</a> · <a href="README.tr.md">TR</a> ·
<a href="README.hi.md">HI</a> · <a href="README.id.md">ID</a> ·
<a href="README.zh.md">ZH</a></sub></p>
