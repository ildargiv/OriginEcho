# OriginEcho

**在 AI 修图之后，还原被抹去的拍摄信息。**

当你把照片送进 AI 生成器或编辑器后，导出的文件通常是「裸」的：相机品牌和型号、
拍摄日期与时间、GPS 坐标、ISO、曝光参数和镜头信息全都被清除。画面看起来没变，
但它的故事已经丢失。

**OriginEcho** 把这段故事还回来。它将原片的全部元数据复制到经 AI 处理后的图
像上，并可选择恢复原文件格式、为结果重新命名。

---

## 它能做什么

| | |
|---|---|
| **复制 EXIF** | 相机、型号、日期/时间、GPS、ISO、曝光、镜头、焦距… |
| **复制 XMP + IPTC** | 说明、作者、关键词、评分、编辑历史 |
| **复制色彩配置文件** | ICC 配置文件，确保颜色准确 |
| **恢复格式** | 把 AI 结果转换为原片格式（PNG → JPEG、WEBP → JPEG…） |
| **重命名结果** | `原名 编辑名.扩展名` |
| **恢复文件日期** | 创建/修改时间与原片一致 |

## 为什么

AI 工具是从零重建文件的，并不了解原片的元数据。OriginEcho 从未被改动的原片中
读取这些数据，再嫁接到处理后的副本上，让成片保留自己的出处。

## 快速开始

1. 双击 **`OriginEcho.bat`**（Windows）——程序窗口打开。
2. 在**原图**中选择未改动的照片（或一个原图文件夹）。
3. 在**已处理照片**中选择 AI 输出（一个文件、多个文件或一个文件夹）。你也可以
   直接把文件**拖拽**到字段中。
4. 点击**开始复制**。

结果会出现在处理过的文件旁，命名为
`<原名> <编辑名>.<原扩展名>`。

### 选项

- **与原图相同格式** —— 转换为原片格式。
- **命名：原图 + 副本** —— 重命名为「原图 + 空格 + 副本」。
- **删除旧文件** —— 重命名成功后删除原副本。
- **复制文件日期** —— 应用原片的创建/修改日期。

## 命令行

```bash
python tools/copy_photo_metadata.py original.jpg edited.jpg [more.jpg ...]
python tools/copy_photo_metadata.py --folder ORIGINALS_DIR EDITED_DIR
```

选项：`--no-icc`、`--no-dates`、`--no-convert`、`--no-rename`、`--keep-old`。

## AI 智能体 (MCP)

OriginEcho 可以作为 **MCP 服务器**（Model Context Protocol）运行，让 AI 助手
—— Claude Desktop、OpenCode、Cursor 等 —— 用自然语言恢复元数据。

以 `--mcp` 标志启动同一个 `OriginEcho.exe`（stdio 传输，仅本地，不开放端口、
不产生网络流量）：

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

从源码运行：`"command": "python", "args": ["C:\\path\\to\\tools\\mcp_server.py"]`

智能体可用的工具：

| 工具 | 作用 |
|---|---|
| `photo_info` | 读取文件的拍摄记录（相机、日期、ISO、GPS……） |
| `restore_metadata` | 将 EXIF/XMP/IPTC/ICC 从原图复制到已编辑照片 |
| `process_folders` | 批量处理两个文件夹 |
| `supported_formats` | 列出支持的格式 |
| `app_info` | 版本与组件检查 |

示例：「把 IMG_20261017_142755.jpg 的元数据移到 Edited 文件夹的所有照片上。」

## 支持的语言

界面提供 **11 种语言** —— 在窗口右上角选择，选择会被记住：

English · Русский · Deutsch · Español · Français · Italiano · Türkçe ·
हिन्दी · Bahasa Indonesia · 한국어 · 中文

## 支持的文件格式

输入/输出：**JPEG、PNG、WEBP、TIFF**。安装 `pillow-heif` 后也支持 HEIC。

## 说明与质量

- 对于 **JPEG → JPEG**，OriginEcho 在字节层面修改文件，因此图像数据
  **无损保留** —— 不会重新压缩。
- 跨格式转换（例如 PNG → JPEG）必然会重新编码图像。
- 透明 PNG/WEBP 转为 JPEG 时会平铺到白色背景。
- PNG 和 WEBP 只能支持部分 EXIF 字段（这是格式本身的限制）。若要完整保存，
  建议使用 JPEG。
- 完整复制（XMP/IPTC）由 **exiftool** 完成（位于 `tools/exiftool`）；缺少它时
  程序仅处理 EXIF + ICC。

## 运行环境要求

- Python 3.11+
- Pillow（缺失时自动安装）
- `tkinterdnd2` —— 拖拽（可选）
- exiftool —— 完整 XMP/IPTC（可选，已附带）

## 致谢

- **exiftool**，Phil Harvey —— 图像元数据领域的黄金标准。
- **Pillow** —— 图像解码/编码。
- **tkinterdnd2** —— 为 Tkinter 提供拖拽支持。

## 许可证

MIT —— 可自由使用和修改。

---

<p align="center"><sub>English: <a href="../README.md">EN</a> ·
<a href="README.ru.md">RU</a> · <a href="README.de.md">DE</a> ·
<a href="README.es.md">ES</a> · <a href="README.fr.md">FR</a> ·
<a href="README.it.md">IT</a> · <a href="README.tr.md">TR</a> ·
<a href="README.hi.md">HI</a> · <a href="README.id.md">ID</a> ·
<a href="README.ko.md">KO</a></sub></p>
