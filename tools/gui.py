# -*- coding: utf-8 -*-
"""Копирование данных фото. Строгий премиум-дизайн: тёмная палитра,
бронзовый акцент, чёткая иерархия и типографика."""
import os
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image

from copy_photo_metadata import (collect_pairs, process_folders, raw_exif,
                                 find_exiftool)

import i18n
from i18n import t as T, LANGS, DEFAULT_LANG, font_family

def _app_dir():
    """Папка для настроек/лога: рядом с программой; в замороженном exe —
    папка рядом с ним, а если она защищена (Program Files) — LocalAppData."""
    if getattr(sys, "frozen", False):
        base = os.path.dirname(os.path.abspath(sys.executable))
        try:
            probe = os.path.join(base, ".wtest")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(probe)
            return base
        except Exception:
            d = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"),
                             "OriginEcho")
            os.makedirs(d, exist_ok=True)
            return d
    return os.path.dirname(os.path.abspath(__file__))


CONFIG = os.path.join(_app_dir(), "lang.cfg")

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND = True
except Exception:
    DND = False

LOG_FILE = os.path.join(_app_dir(), "errors.log")

BG, PANEL, PANEL2 = "#101318", "#171b22", "#1c2129"
LINE = "#2a303a"
ACCENT, ACCENT2 = "#e2b35c", "#f0c67a"
INK, MUT, DIM = "#eaeef3", "#94a0b0", "#67707e"
OK, ERR, WARN = "#6fcf97", "#f2705b", "#d9a55c"

F = ("Segoe UI", 9); FS = ("Segoe UI", 8); CAPS = ("Segoe UI", 8, "bold")
H = ("Segoe UI", 10, "bold"); LT = ("Segoe UI", 19, "bold"); MONO = ("Consolas", 9)

IMG_TYPES = [("Фотографии", "*.jpg *.jpeg *.png *.webp *.tif *.tiff *.heic"),
             ("Все файлы", "*.*")]


def log_error(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as fh:
            fh.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def _excepthook(tp, val, tb):
    import traceback
    log_error("ОШИБКА:\n" + "".join(traceback.format_exception(tp, val, tb)))
    sys.__excepthook__(tp, val, tb)


sys.excepthook = _excepthook


def read_summary(path, lang=None):
    try:
        with Image.open(path) as im:
            e = im.getexif()
        parts = []
        make = str(e.get(271, "") or "").strip()
        model = str(e.get(272, "") or "").strip()
        if make or model:
            parts.append(f"{make} {model}".strip())
        dt = str(e.get(306, "") or "").strip()
        if dt:
            parts.append(dt.replace(":", ".", 1)[:19])
        if e.get(0x8827):
            parts.append(f"ISO {e.get(0x8827)}")
        base = f"{im.size[0]}x{im.size[1]}"
        return ("   |   ".join(parts) + "   |   " + base) if parts \
            else T("summary_none", lang), INK
    except Exception:
        return T("summary_fail", lang), DIM


class App:
    def __init__(self, root):
        self.root = root
        self.lang = self._load_lang()
        self.fam = font_family(self.lang)
        root.title(T("app_title", self.lang))
        root.configure(bg=BG)
        root.geometry("920x700")
        root.minsize(800, 580)
        root.report_callback_exception = self._report_err
        self._init_vars()
        self._build()
        self._setup_dnd()

    def _load_lang(self):
        try:
            with open(CONFIG, "r", encoding="utf-8") as fh:
                c = fh.read().strip()
            return c if c in LANGS else DEFAULT_LANG
        except Exception:
            return DEFAULT_LANG

    def _save_lang(self):
        try:
            with open(CONFIG, "w", encoding="utf-8") as fh:
                fh.write(self.lang)
        except Exception:
            pass

    def _init_vars(self):
        self.src_var = tk.StringVar()
        self.dst_var = tk.StringVar()
        self.v_to_fmt = tk.BooleanVar(value=True)
        self.v_ren = tk.BooleanVar(value=True)
        self.v_del = tk.BooleanVar(value=True)
        self.v_dates = tk.BooleanVar(value=True)

    def _report_err(self, typ, val, tb):
        import traceback
        log_error("ОШИБКА В ОКНЕ:\n" + "".join(traceback.format_exception(typ, val, tb)))
        try:
            messagebox.showerror(T("err_prog", self.lang),
                                 f"{val}\n\n— tools\\errors.log")
        except Exception:
            pass

    # ---------------- сборка ----------------
    def _font(self, size=9, weight=""):
        return (self.fam, size, weight) if weight else (self.fam, size)

    def _build(self):
        outer = tk.Frame(self.root, bg=BG)
        outer.pack(fill="both", expand=True, padx=30, pady=24)

        # верх: заголовок + выбор языка
        top = tk.Frame(outer, bg=BG)
        top.pack(fill="x", pady=(0, 16))
        lt = tk.Frame(top, bg=BG)
        lt.pack(side="left", fill="x", expand=True)
        tk.Label(lt, text=i18n.LANGS and i18n.EN["app_name"].upper(), bg=BG,
                 fg=INK, font=self._font(19, "bold")).pack(anchor="w")
        tk.Label(lt, text=T("tagline", self.lang), bg=BG, fg=MUT,
                 font=self._font()).pack(anchor="w", pady=(4, 0))
        # выбор языка
        lang_row = tk.Frame(top, bg=BG)
        lang_row.pack(side="right", anchor="ne")
        tk.Label(lang_row, text=T("lang_label", self.lang), bg=BG, fg=DIM,
                 font=self._font(8)).pack(side="left", padx=(0, 8))
        rev = {v: k for k, v in LANGS.items()}
        mb = tk.Menubutton(lang_row, text=LANGS[self.lang], bg=PANEL2, fg=INK,
                           activebackground=PANEL, activeforeground=INK,
                           font=self._font(9), relief="flat", highlightthickness=1,
                           highlightbackground=LINE, indicatoron=True, anchor="w",
                           width=16)
        mb.pack()
        menu = tk.Menu(mb, tearoff=0, bg=PANEL2, fg=INK, activebackground=ACCENT,
                       activeforeground="#131009", font=self._font(9))
        for code, name in LANGS.items():
            menu.add_command(label=name,
                             command=lambda c=code: self._change_lang(c))
        mb.config(menu=menu)
        tk.Frame(outer, bg=LINE, height=1).pack(fill="x", pady=(0, 18))

        self._card(outer, "01", T("c1_title", self.lang),
                   T("c1_sub", self.lang), self._build_src).pack(fill="x",
                                                                 pady=(0, 12))
        self._card(outer, "02", T("c2_title", self.lang),
                   T("c2_sub", self.lang), self._build_dst).pack(fill="x",
                                                                  pady=(0, 12))
        self._card(outer, "03", T("c3_title", self.lang),
                   T("c3_sub", self.lang), self._build_go).pack(fill="both",
                                                                expand=True)

    def _change_lang(self, code):
        if code and code != self.lang:
            self.lang = code
            self._save_lang()
            self._rebuild()

    def _rebuild(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.title(T("app_title", self.lang))
        self._build()
        self._setup_dnd()

    def _card(self, parent, num, title, sub, fn):
        card = tk.Frame(parent, bg=PANEL, highlightthickness=1,
                        highlightbackground=LINE)
        head = tk.Frame(card, bg=PANEL)
        head.pack(fill="x", padx=16, pady=(12, 6))
        tk.Label(head, text=num, bg=PANEL, fg=ACCENT,
                 font=self._font(12, "bold"), width=2, anchor="w").pack(side="left")
        col = tk.Frame(head, bg=PANEL)
        col.pack(side="left", padx=(8, 0), anchor="n")
        tk.Label(col, text=title.upper(), bg=PANEL, fg=INK,
                 font=self._font(8, "bold")).pack(anchor="w")
        if sub:
            tk.Label(col, text=sub, bg=PANEL, fg=MUT,
                     font=self._font(8)).pack(anchor="w")
        body = tk.Frame(card, bg=PANEL)
        body.pack(fill="x", padx=16, pady=(0, 14))
        fn(body)
        return card

    def _field(self, body, var, on_file, on_dir):
        row = tk.Frame(body, bg=PANEL)
        row.pack(fill="x")
        box = tk.Frame(row, bg=LINE, highlightthickness=1,
                       highlightbackground=LINE)
        box.pack(side="left", fill="x", expand=True)
        ent = tk.Entry(box, textvariable=var, bg=PANEL2, fg=INK,
                       insertbackground=ACCENT, relief="flat",
                       font=self._font(), highlightthickness=0)
        ent.pack(fill="x", padx=8, ipady=6)
        for lbl, cmd in ((T("btn_file", self.lang), on_file),
                         (T("btn_folder", self.lang), on_dir)):
            tk.Button(row, text=lbl, command=cmd, bg=PANEL2, fg=MUT,
                      activebackground=PANEL, activeforeground=INK,
                      relief="flat", font=self._font(8, "bold"), padx=10,
                      pady=6, cursor="hand2", highlightthickness=1,
                      highlightbackground=LINE).pack(side="left", padx=(6, 0))
        return ent

    def _build_src(self, body):
        self.src_ent = self._field(body, self.src_var,
                                   self.pick_src_file, self.pick_src_dir)
        self.src_summary = tk.Label(body, text="", bg=PANEL, fg=DIM,
                                    font=MONO, anchor="w")
        self.src_summary.pack(fill="x", pady=(8, 0))

    def _build_dst(self, body):
        self.dst_ent = self._field(body, self.dst_var,
                                  self.pick_dst_files, self.pick_dst_dir)
        opts = tk.Frame(body, bg=PANEL)
        opts.pack(fill="x", pady=(10, 0))
        for col, (var, key) in enumerate([
                (self.v_to_fmt, "opt_format"), (self.v_ren, "opt_rename"),
                (self.v_del, "opt_delete"), (self.v_dates, "opt_dates")]):
            tk.Checkbutton(opts, text=T(key, self.lang), variable=var,
                           bg=PANEL, fg=MUT, selectcolor=PANEL,
                           activebackground=PANEL, activeforeground=INK,
                           font=self._font(8), relief="flat",
                           highlightthickness=0).grid(row=0, column=col,
                                                      sticky="w", padx=(0, 18))

    def _build_go(self, body):
        has = bool(find_exiftool())
        meta = T("meta_on" if has else "meta_off", self.lang)
        info = T("hint", self.lang).format(meta=meta)
        tk.Label(body, text=info, bg=PANEL, fg=MUT, font=self._font(8),
                 anchor="w").pack(fill="x", pady=(0, 8))
        btn = tk.Button(body, text=T("btn_run", self.lang), command=self.run,
                        bg=ACCENT, fg="#131009", activebackground=ACCENT2,
                        activeforeground="#131009", relief="flat",
                        font=self._font(10, "bold"), padx=16, pady=10,
                        cursor="hand2", highlightthickness=0)
        btn.pack(fill="x")
        box = tk.Frame(body, bg=LINE, highlightthickness=1,
                       highlightbackground=LINE)
        box.pack(fill="both", expand=True, pady=(10, 0))
        self.log = tk.Text(box, height=9, state="disabled", wrap="word",
                           bg=PANEL2, fg=INK, font=(self.fam, 9), relief="flat",
                           insertbackground=ACCENT, highlightthickness=0,
                           padx=8, pady=6)
        self.log.pack(fill="both", expand=True)

    # ---------------- перетаскивание ----------------
    def _setup_dnd(self):
        if not DND:
            return
        for w, tgt in ((self.src_ent, "src"), (self.dst_ent, "dst")):
            w.drop_target_register(DND_FILES)
            w.dnd_bind("<<Drop>>", lambda e, t=tgt: self._on_drop(e, t))

    def _on_drop(self, event, target):
        raw = event.data
        paths = []
        i = 0
        while i < len(raw):
            if raw[i] == "{":
                j = raw.find("}", i)
                paths.append(raw[i + 1:j]); i = j + 1
            else:
                j = raw.find(" ", i)
                if j == -1:
                    paths.append(raw[i:]); i = len(raw)
                else:
                    paths.append(raw[i:j]); i = j
            while i < len(raw) and raw[i] == " ":
                i += 1
        paths = [p for p in paths if p]
        if not paths:
            return
        if target == "src":
            self.src_var.set(" ".join(paths))
            if len(paths) == 1 and os.path.isfile(paths[0]):
                self._preview_src(paths[0])
        else:
            self.dst_var.set(" | ".join(paths))

    # ---------------- выборы ----------------
    def pick_src_file(self):
        p = filedialog.askopenfilename(title="Оригинальная фотография",
                                       filetypes=IMG_TYPES)
        if p:
            self.src_var.set(p)
            self._preview_src(p)

    def pick_src_dir(self):
        p = filedialog.askdirectory(title="Папка с оригиналами")
        if p:
            self.src_var.set(p)

    def pick_dst_files(self):
        ps = filedialog.askopenfilenames(title="Обработанные фотографии",
                                         filetypes=IMG_TYPES)
        if ps:
            self.dst_var.set(" | ".join(ps))

    def pick_dst_dir(self):
        p = filedialog.askdirectory(title="Папка с обработанными фото")
        if p:
            self.dst_var.set(p)

    def _preview_src(self, path):
        if hasattr(self, "src_summary"):
            txt, color = read_summary(path, self.lang)
            self.src_summary.configure(text=txt, fg=color)

    # ---------------- лог ----------------
    def write(self, entries):
        self.log.configure(state="normal")
        for ok, line in entries:
            color = OK if ok else (ERR if "ОШИБКА" in line else WARN)
            self.log.insert("end", line + "\n", ("c",))
            self.log.tag_configure("c", foreground=color)
        self.log.see("end")
        self.log.configure(state="disabled")

    # ---------------- запуск ----------------
    def run(self):
        src = self.src_var.get().strip()
        dst_raw = self.dst_var.get().strip()
        if not src or not dst_raw:
            messagebox.showwarning(T("warn_title", self.lang),
                                   T("warn_nothing", self.lang))
            return
        dsts = [d for d in dst_raw.split(" | ") if d]
        kws = dict(to_src_format=self.v_to_fmt.get(), rename=self.v_ren.get(),
                   delete_old=self.v_del.get(), copy_dates=self.v_dates.get(),
                   lang=self.lang)

        def work():
            try:
                if os.path.isdir(src) and os.path.isdir(dsts[0]):
                    entries = process_folders(src, dsts[0], **kws)
                elif os.path.isfile(src):
                    entries = collect_pairs(src, dsts, **kws)
                else:
                    entries = [(False, "[!] " + T("err_kinds", self.lang))]
                self.root.after(0, self.write, entries)
            except Exception as e:
                import traceback
                log_error("ОШИБКА ОБРАБОТКИ:\n" + traceback.format_exc())
                self.root.after(0, self.write,
                                [(False, f"[ОШИБКА] {e} — log: tools\\errors.log")])

        self.write([(True, T("log_start", self.lang))])
        threading.Thread(target=work, daemon=True).start()


def main():
    # exe собирается с консолью (нужно для режима --mcp), но в GUI-режиме
    # окно консоли сразу скрываем, чтобы двойной клик давал «чистое» окно
    if getattr(sys, "frozen", False):
        try:
            import ctypes
            h = ctypes.windll.kernel32.GetConsoleWindow()
            if h:
                ctypes.windll.user32.ShowWindow(h, 0)  # SW_HIDE
        except Exception:
            pass
    root = TkinterDnD.Tk() if DND else tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    if "--mcp" in sys.argv:
        # режим MCP-сервера для ИИ-агентов: OriginEcho.exe --mcp (stdio)
        import mcp_server
        sys.exit(mcp_server.main())
    main()

