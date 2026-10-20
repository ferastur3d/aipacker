import os
import sys
import re
import json
import fnmatch
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Soporte para DPI alto en Windows (evita textos borrosos)
if sys.platform.startswith('win'):
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

CONFIG_FILE = "aipacker_config.json"

ALLOWED_EXTENSIONS = {
    # Flutter / Dart / Android / iOS
    '.dart', '.yaml', '.yml', '.kts', '.gradle', '.properties', '.xml', 
    '.swift', '.kt', '.java', '.plist', '.xcconfig',
    # Web / Frontend / Backend
    '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.vue', '.svelte', '.php',
    # Python & Data
    '.py', '.pyw', '.ipynb', '.json', '.csv', '.tsv', '.sql',
    # C, C++, C#, Rust, Go, etc.
    '.c', '.cpp', '.h', '.hpp', '.cs', '.rs', '.go', '.rb', '.lua', '.pl',
    # Scripts y configs
    '.sh', '.bash', '.bat', '.cmd', '.ps1', '.ini', '.cfg', '.conf', 
    '.toml', '.env.example',
    # Docs
    '.txt', '.md', '.rst'
}

ALLOWED_EXACT_NAMES = {
    'dockerfile', 'makefile', 'gemfile', 'podfile', 'license', 'readme', '.gitignore'
}

IGNORED_DIRS = {
    '.git', '.svn', '.hg',
    'build', '.dart_tool', '.gradle', 'pods', '.symlinks', '.idea',
    'node_modules', '.next', '.nuxt', 'dist', 'out',
    '__pycache__', '.venv', 'venv', 'env', '.pytest_cache',
    'target', 'bin', 'obj', '.vscode'
}

ICON_CHECKED = "☑"
ICON_UNCHECKED = "☐"
ICON_PARTIAL = "▣"

LANGUAGES = {
    "English": {
        "title": "AIPacker Pro - AI Context Bundler",
        "subtitle": "Package your project source code into a clean AI-ready prompt",
        "step1": "Step 1: Choose project folder",
        "browse": "Browse...",
        "reload": "Reload",
        "step2": "Step 2: Select files & folders (Double click to preview file)",
        "col_name": "Name",
        "col_sel_size": "Selected Size",
        "col_tot_size": "Total Size",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "search": "Filter:",
        "step3": "Step 3: Export Context",
        "filename": "Output filename:",
        "btn_process": "🚀 Process & Export Context",
        "btn_copy": "📋 Copy to Clipboard",
        "stats": "Selected Files: {files} | Package Size: {sel_size} | Total Repo: {tot_size} | Est. Tokens: ~{tokens:,}",
        "status_ready": "Ready.",
        "status_loading": "Scanning project tree and calculating sizes...",
        "status_success": "Packaged successfully into '{file}'!",
        "err_dir": "Please select a valid directory.",
        "err_no_files": "No files selected. Please mark at least one file.",
        "tree_header": "Selected Directory Tree:",
        "file_header": "FILE: {path}",
        "preview_title": "Preview: {file}",
        "modal_title": "Bundle Successfully Generated!",
        "modal_heading": "Your AI Context file is ready!",
        "modal_info": "• File Name: {name}\n• Included Files: {count}\n• Output Size: {size}\n• Estimated Tokens: ~{tokens:,}\n• Location: {path}",
        "btn_open_file": "📄 Open File",
        "btn_open_folder": "📁 Open Folder",
        "btn_modal_copy": "📋 Copy Content",
        "btn_close": "Close",
        "copied": "Content copied to clipboard!"
    },
    "Español": {
        "title": "AIPacker Pro - Empaquetador para IA",
        "subtitle": "Empaqueta el código de tu proyecto en un archivo óptimo para LLMs",
        "step1": "Paso 1: Selecciona la carpeta del proyecto",
        "browse": "Examinar...",
        "reload": "Recargar",
        "step2": "Paso 2: Marca archivos y carpetas (Doble clic para previsualizar)",
        "col_name": "Nombre",
        "col_sel_size": "Tamaño Seleccionado",
        "col_tot_size": "Tamaño Total",
        "select_all": "Marcar Todo",
        "deselect_all": "Desmarcar Todo",
        "search": "Filtrar:",
        "step3": "Paso 3: Exportar Contexto",
        "filename": "Nombre del archivo:",
        "btn_process": "🚀 Procesar y Empaquetar",
        "btn_copy": "📋 Copiar al Portapapeles",
        "stats": "Archivos Marcados: {files} | Tamaño Paquete: {sel_size} | Total Carpeta: {tot_size} | Tokens Est.: ~{tokens:,}",
        "status_ready": "Listo.",
        "status_loading": "Escaneando estructura y calculando pesos...",
        "status_success": "¡Empaquetado con éxito en '{file}'!",
        "err_dir": "Por favor, selecciona una carpeta válida.",
        "err_no_files": "No hay archivos seleccionados. Marca al menos uno.",
        "tree_header": "Árbol de directorios seleccionados:",
        "file_header": "ARCHIVO: {path}",
        "preview_title": "Previsualización: {file}",
        "modal_title": "¡Paquete Generado con Éxito!",
        "modal_heading": "¡El contexto para la IA está listo!",
        "modal_info": "• Archivo: {name}\n• Archivos Incluidos: {count}\n• Tamaño del Paquete: {size}\n• Tokens Estimados: ~{tokens:,}\n• Ruta: {path}",
        "btn_open_file": "📄 Abrir Archivo",
        "btn_open_folder": "📁 Abrir Carpeta",
        "btn_modal_copy": "📋 Copiar Contenido",
        "btn_close": "Cerrar",
        "copied": "¡Contenido copiado al portapapeles!"
    },
    "Deutsch": {
        "title": "AIPacker Pro - KI-Kontextpacker",
        "subtitle": "Packen Sie Ihren Code in eine optimale Datei für LLMs",
        "step1": "Schritt 1: Projektordner auswählen",
        "browse": "Durchsuchen...",
        "reload": "Neu laden",
        "step2": "Schritt 2: Dateien auswählen (Doppelklick für Vorschau)",
        "col_name": "Name",
        "col_sel_size": "Ausgewählte Größe",
        "col_tot_size": "Gesamtgröße",
        "select_all": "Alle auswählen",
        "deselect_all": "Alle abwählen",
        "search": "Filter:",
        "step3": "Schritt 3: Kontext exportieren",
        "filename": "Dateiname:",
        "btn_process": "🚀 Verarbeiten & Packen",
        "btn_copy": "📋 In die Zwischenablage kopieren",
        "stats": "Dateien: {files} | Paketgröße: {sel_size} | Gesamt: {tot_size} | Tokens: ~{tokens:,}",
        "status_ready": "Bereit.",
        "status_loading": "Projektstruktur wird gescannt...",
        "status_success": "Erfolgreich gepackt in '{file}'!",
        "err_dir": "Bitte wählen Sie einen gültigen Ordner.",
        "err_no_files": "Keine Dateien ausgewählt.",
        "tree_header": "Ausgewählter Verzeichnisbaum:",
        "file_header": "DATEI: {path}",
        "preview_title": "Vorschau: {file}",
        "modal_title": "Paket erfolgreich erstellt!",
        "modal_heading": "Ihr KI-Kontext ist bereit!",
        "modal_info": "• Datei: {name}\n• Enthaltene Dateien: {count}\n• Dateigröße: {size}\n• Geschätzte Tokens: ~{tokens:,}\n• Pfad: {path}",
        "btn_open_file": "📄 Datei öffnen",
        "btn_open_folder": "📁 Ordner öffnen",
        "btn_modal_copy": "📋 Inhalt kopieren",
        "btn_close": "Schließen",
        "copied": "In die Zwischenablage kopiert!"
    },
    "Français": {
        "title": "AIPacker Pro - Empaqueteur pour IA",
        "subtitle": "Regroupez votre code dans un fichier de contexte pour LLM",
        "step1": "Étape 1: Choisissez le dossier du projet",
        "browse": "Parcourir...",
        "reload": "Recharger",
        "step2": "Étape 2: Sélectionnez les fichiers (double-clic pour prévisualiser)",
        "col_name": "Nom",
        "col_sel_size": "Taille Sélectionnée",
        "col_tot_size": "Taille Totale",
        "select_all": "Tout sélectionner",
        "deselect_all": "Tout désélectionner",
        "search": "Filtrer:",
        "step3": "Étape 3: Exporter le contexte",
        "filename": "Nom du fichier:",
        "btn_process": "🚀 Traiter et Empaqueter",
        "btn_copy": "📋 Copier dans le presse-papiers",
        "stats": "Fichiers: {files} | Sélection: {sel_size} | Total: {tot_size} | Tokens: ~{tokens:,}",
        "status_ready": "Prêt.",
        "status_loading": "Analyse de la structure...",
        "status_success": "Empaqueté avec succès dans '{file}'!",
        "err_dir": "Veuillez choisir un dossier valide.",
        "err_no_files": "Aucun fichier sélectionné.",
        "tree_header": "Arborescence sélectionnée:",
        "file_header": "FICHIER: {path}",
        "preview_title": "Aperçu: {file}",
        "modal_title": "Paquet généré avec succès!",
        "modal_heading": "Votre contexte IA est prêt!",
        "modal_info": "• Fichier: {name}\n• Fichiers inclus: {count}\n• Taille: {size}\n• Tokens estimés: ~{tokens:,}\n• Emplacement: {path}",
        "btn_open_file": "📄 Ouvrir le fichier",
        "btn_open_folder": "📁 Ouvrir le dossier",
        "btn_modal_copy": "📋 Copier le contenu",
        "btn_close": "Fermer",
        "copied": "Copié dans le presse-papiers!"
    },
    "Italiano": {
        "title": "AIPacker Pro - Impacchettatore per IA",
        "subtitle": "Raggruppa il codice del tuo progetto per i modelli LLM",
        "step1": "Passo 1: Seleziona la cartella del progetto",
        "browse": "Sfoglia...",
        "reload": "Ricarica",
        "step2": "Passo 2: Seleziona file e cartelle (doppio clic per anteprima)",
        "col_name": "Nome",
        "col_sel_size": "Dimensione Selezionata",
        "col_tot_size": "Dimensione Totale",
        "select_all": "Seleziona tutto",
        "deselect_all": "Deseleziona tutto",
        "search": "Filtra:",
        "step3": "Passo 3: Esporta contesto",
        "filename": "Nome file:",
        "btn_process": "🚀 Elabora e Confeziona",
        "btn_copy": "📋 Copia negli appunti",
        "stats": "File: {files} | Dimensione: {sel_size} | Totale: {tot_size} | Token: ~{tokens:,}",
        "status_ready": "Pronto.",
        "status_loading": "Scansione della cartella...",
        "status_success": "Impacchettato con successo in '{file}'!",
        "err_dir": "Seleziona una cartella valida.",
        "err_no_files": "Nessun file selezionato.",
        "tree_header": "Albero directory selezionate:",
        "file_header": "FILE: {path}",
        "preview_title": "Anteprima: {file}",
        "modal_title": "Pacchetto Generato con Successo!",
        "modal_heading": "Il tuo contesto per IA è pronto!",
        "modal_info": "• File: {name}\n• File inclusi: {count}\n• Dimensione: {size}\n• Token stimati: ~{tokens:,}\n• Percorso: {path}",
        "btn_open_file": "📄 Apri File",
        "btn_open_folder": "📁 Apri Cartella",
        "btn_modal_copy": "📋 Copia Contenuto",
        "btn_close": "Chiudi",
        "copied": "Copiato negli appunti!"
    },
    "Português": {
        "title": "AIPacker Pro - Empacotador para IA",
        "subtitle": "Reúna o código do seu projeto em um arquivo ideal para LLMs",
        "step1": "Passo 1: Selecione a pasta do projeto",
        "browse": "Procurar...",
        "reload": "Recarregar",
        "step2": "Passo 2: Selecione arquivos e pastas (duplo clique para visualizar)",
        "col_name": "Nome",
        "col_sel_size": "Tamanho Selecionado",
        "col_tot_size": "Tamanho Total",
        "select_all": "Marcar Tudo",
        "deselect_all": "Desmarcar Tudo",
        "search": "Filtrar:",
        "step3": "Passo 3: Exportar Contexto",
        "filename": "Nome do arquivo:",
        "btn_process": "🚀 Processar e Empacotar",
        "btn_copy": "📋 Copiar para Área de Transferência",
        "stats": "Arquivos: {files} | Tamanho Selecionado: {sel_size} | Total: {tot_size} | Tokens: ~{tokens:,}",
        "status_ready": "Pronto.",
        "status_loading": "Escaneando estrutura...",
        "status_success": "Empacotado com sucesso em '{file}'!",
        "err_dir": "Selecione uma pasta válida.",
        "err_no_files": "Nenhum arquivo selecionado.",
        "tree_header": "Árvore de diretórios selecionados:",
        "file_header": "ARQUIVO: {path}",
        "preview_title": "Visualização: {file}",
        "modal_title": "Pacote Criado com Sucesso!",
        "modal_heading": "Seu arquivo de contexto para IA está pronto!",
        "modal_info": "• Arquivo: {name}\n• Arquivos Incluídos: {count}\n• Tamanho: {size}\n• Tokens Estimados: ~{tokens:,}\n• Caminho: {path}",
        "btn_open_file": "📄 Abrir Arquivo",
        "btn_open_folder": "📁 Abrir Pasta",
        "btn_modal_copy": "📋 Copiar Conteúdo",
        "btn_close": "Fechar",
        "copied": "Copiado para a área de transferência!"
    }
}

def format_bytes(bytes_qty):
    """Convierte bytes a formato legible (B, KB, MB)."""
    if bytes_qty < 1024:
        return f"{bytes_qty} B"
    elif bytes_qty < 1024 * 1024:
        return f"{bytes_qty / 1024:.1f} KB"
    else:
        return f"{bytes_qty / (1024 * 1024):.2f} MB"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AIPackerApp:
    def __init__(self, root, cli_dir=None):
        self.root = root
        self.root.geometry("1000x750")
        self.root.minsize(820, 600)

        self.config = self.load_config()
        self.current_lang = self.config.get("language", "English")
        if self.current_lang not in LANGUAGES:
            self.current_lang = "English"

        self.target_dir = ""
        self.item_data = {}  # id: dict(path, rel_path, is_dir, checked, file_size, total_size, sel_size, name)
        self.last_generated_content = ""
        self.last_generated_file = ""
        self.gitignore_patterns = []

        self._load_app_icons()
        self._setup_ui()
        self.apply_language()

        # Prioridad de carga: argumento CLI > última carpeta usada
        target = cli_dir if (cli_dir and os.path.isdir(cli_dir)) else self.config.get("last_directory", "")
        if target and os.path.isdir(target):
            self.load_directory(os.path.abspath(target))

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"language": "English", "last_directory": ""}

    def save_config(self):
        self.config["language"] = self.current_lang
        self.config["last_directory"] = self.target_dir
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception:
            pass

    def t(self, key):
        return LANGUAGES.get(self.current_lang, LANGUAGES["English"]).get(key, key)

    def _load_app_icons(self):
        ico = resource_path("icon.ico")
        if os.path.exists(ico):
            try:
                self.root.iconbitmap(ico)
            except Exception:
                pass

    def _setup_ui(self):
        # Cabecera
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)

        png = resource_path("icon.png")
        if os.path.exists(png):
            try:
                self.icon_img = tk.PhotoImage(file=png)
                # Si la imagen es grande (ej. 1024x1024), la reducimos con subsample nativo
                if self.icon_img.width() > 64:
                    factor = max(1, self.icon_img.width() // 46)
                    self.icon_img = self.icon_img.subsample(factor, factor)
                ttk.Label(header_frame, image=self.icon_img).pack(side=tk.LEFT, padx=(0, 10))
            except Exception:
                pass

        title_box = ttk.Frame(header_frame)
        title_box.pack(side=tk.LEFT)
        self.lbl_title = ttk.Label(title_box, font=("Segoe UI", 14, "bold"))
        self.lbl_title.pack(anchor="w")
        self.lbl_subtitle = ttk.Label(title_box, foreground="#555")
        self.lbl_subtitle.pack(anchor="w")

        lang_box = ttk.Frame(header_frame)
        lang_box.pack(side=tk.RIGHT, padx=5)
        ttk.Label(lang_box, text="🌐").pack(side=tk.LEFT, padx=(0, 3))
        self.lang_combo = ttk.Combobox(lang_box, values=list(LANGUAGES.keys()), state="readonly", width=12)
        self.lang_combo.set(self.current_lang)
        self.lang_combo.pack(side=tk.LEFT)
        self.lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)

        # Paso 1: Directorio
        self.frame_step1 = ttk.LabelFrame(self.root, padding=8)
        self.frame_step1.pack(fill=tk.X, padx=10, pady=4)

        self.path_entry = ttk.Entry(self.frame_step1)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        self.btn_browse = ttk.Button(self.frame_step1, command=self.choose_directory)
        self.btn_browse.pack(side=tk.RIGHT, padx=2)
        self.btn_reload = ttk.Button(self.frame_step1, command=self.reload_directory)
        self.btn_reload.pack(side=tk.RIGHT, padx=2)

        # Paso 2: Selección y Árbol con columnas
        self.frame_step2 = ttk.LabelFrame(self.root, padding=8)
        self.frame_step2.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        toolbar = ttk.Frame(self.frame_step2)
        toolbar.pack(fill=tk.X, pady=(0, 6))

        self.btn_select_all = ttk.Button(toolbar, command=lambda: self.toggle_all(True))
        self.btn_select_all.pack(side=tk.LEFT, padx=2)
        self.btn_deselect_all = ttk.Button(toolbar, command=lambda: self.toggle_all(False))
        self.btn_deselect_all.pack(side=tk.LEFT, padx=2)

        self.lbl_search = ttk.Label(toolbar)
        self.lbl_search.pack(side=tk.LEFT, padx=(15, 3))

        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_tree)
        self.search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=22)
        self.search_entry.pack(side=tk.LEFT, padx=2)

        self.stats_label = ttk.Label(toolbar, font=("Segoe UI", 9, "bold"))
        self.stats_label.pack(side=tk.RIGHT, padx=5)

        # Treeview de 3 columnas
        tree_container = ttk.Frame(self.frame_step2)
        tree_container.pack(fill=tk.BOTH, expand=True)

        tree_scroll = ttk.Scrollbar(tree_container)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_container,
            columns=("sel_size", "tot_size"),
            yscrollcommand=tree_scroll.set,
            selectmode="browse"
        )
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.tree.yview)

        self.tree.column("#0", width=550, stretch=True)
        self.tree.column("sel_size", width=140, anchor="e")
        self.tree.column("tot_size", width=140, anchor="e")

        self.tree.bind('<Button-1>', self.on_tree_click)
        self.tree.bind('<Double-1>', self.on_tree_double_click)

        # Paso 3: Exportar
        self.frame_step3 = ttk.LabelFrame(self.root, padding=8)
        self.frame_step3.pack(fill=tk.X, padx=10, pady=4)

        self.lbl_filename = ttk.Label(self.frame_step3)
        self.lbl_filename.pack(side=tk.LEFT, padx=(0, 6))

        self.out_name_entry = ttk.Entry(self.frame_step3, width=22)
        self.out_name_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_process = ttk.Button(self.frame_step3, command=self.process_files)
        self.btn_process.pack(side=tk.RIGHT, padx=2)

        self.btn_copy = ttk.Button(self.frame_step3, command=self.copy_to_clipboard, state="disabled")
        self.btn_copy.pack(side=tk.RIGHT, padx=4)

        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w', padding=4)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def apply_language(self):
        self.root.title(self.t("title"))
        self.lbl_title.config(text=self.t("title"))
        self.lbl_subtitle.config(text=self.t("subtitle"))

        self.frame_step1.config(text=f" {self.t('step1')} ")
        self.btn_browse.config(text=self.t("browse"))
        self.btn_reload.config(text=self.t("reload"))

        self.frame_step2.config(text=f" {self.t('step2')} ")
        self.btn_select_all.config(text=self.t("select_all"))
        self.btn_deselect_all.config(text=self.t("deselect_all"))
        self.lbl_search.config(text=self.t("search"))

        self.tree.heading('#0', text=self.t("col_name"), anchor='w')
        self.tree.heading('sel_size', text=self.t("col_sel_size"), anchor='e')
        self.tree.heading('tot_size', text=self.t("col_tot_size"), anchor='e')

        self.frame_step3.config(text=f" {self.t('step3')} ")
        self.lbl_filename.config(text=self.t("filename"))
        self.btn_process.config(text=self.t("btn_process"))
        self.btn_copy.config(text=self.t("btn_copy"))

        if not self.target_dir:
            self.status_var.set(self.t("status_ready"))
        self.update_stats()

    def on_language_change(self, event):
        self.current_lang = self.lang_combo.get()
        self.save_config()
        self.apply_language()

    def _load_gitignore(self, base_dir):
        self.gitignore_patterns = []
        git_path = os.path.join(base_dir, ".gitignore")
        if os.path.exists(git_path):
            try:
                with open(git_path, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            self.gitignore_patterns.append(line.rstrip("/"))
            except Exception:
                pass

    def is_gitignored(self, name):
        for pattern in self.gitignore_patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        return False

    def choose_directory(self):
        folder = filedialog.askdirectory(initialdir=self.target_dir or os.getcwd(), title=self.t("step1"))
        if folder:
            self.load_directory(folder)

    def reload_directory(self):
        path = self.path_entry.get().strip()
        if os.path.isdir(path):
            self.load_directory(path)
        else:
            messagebox.showerror("Error", self.t("err_dir"))

    def get_next_output_filename(self, base_path):
        max_idx = 0
        pattern = re.compile(r"^total_(\d+)\.txt$", re.IGNORECASE)
        try:
            for item in os.listdir(base_path):
                match = pattern.match(item)
                if match:
                    max_idx = max(max_idx, int(match.group(1)))
        except Exception:
            pass
        return f"total_{max_idx + 1}.txt"

    def is_valid_file(self, filename):
        if filename.startswith("total_") and filename.endswith(".txt"):
            return False
        lower = filename.lower()
        if lower in ALLOWED_EXACT_NAMES:
            return True
        _, ext = os.path.splitext(lower)
        return ext in ALLOWED_EXTENSIONS

    def load_directory(self, folder_path):
        self.target_dir = os.path.abspath(folder_path)
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, self.target_dir)

        self.save_config()
        self._load_gitignore(self.target_dir)

        self.out_name_entry.delete(0, tk.END)
        self.out_name_entry.insert(0, self.get_next_output_filename(self.target_dir))

        self.tree.delete(*self.tree.get_children())
        self.item_data.clear()

        self.status_var.set(self.t("status_loading"))
        self.root.update_idletasks()

        root_id = self._populate_tree(self.target_dir, "")
        if root_id:
            # Calcular tamaños acumulados
            self._recalculate_folder_sizes(root_id)
            self._refresh_tree_display(root_id)
            self.tree.item(root_id, open=True)

        self.update_stats()
        self.status_var.set(f"{self.t('status_ready')} ({self.target_dir})")
        self.btn_copy.config(state="disabled")

    def _populate_tree(self, current_path, parent_id):
        """Puebla el árbol garantizando que todos los elementos inicien seleccionados (checked=True)."""
        base_name = os.path.basename(current_path) if parent_id else current_path
        node_id = self.tree.insert(parent_id, "end", text="", open=False)

        self.item_data[node_id] = {
            "path": current_path,
            "rel_path": os.path.relpath(current_path, self.target_dir),
            "is_dir": True,
            "checked": True,
            "file_size": 0,
            "total_size": 0,
            "sel_size": 0,
            "name": base_name
        }

        try:
            entries = sorted(os.scandir(current_path), key=lambda e: (not e.is_dir(), e.name.lower()))
            for entry in entries:
                if entry.is_dir():
                    if entry.name.lower() in IGNORED_DIRS or self.is_gitignored(entry.name):
                        continue
                    self._populate_tree(entry.path, node_id)
                elif entry.is_file():
                    if self.is_valid_file(entry.name) and not self.is_gitignored(entry.name):
                        size = entry.stat().st_size
                        f_id = self.tree.insert(node_id, "end", text="")
                        self.item_data[f_id] = {
                            "path": entry.path,
                            "rel_path": os.path.relpath(entry.path, self.target_dir),
                            "is_dir": False,
                            "checked": True,
                            "file_size": size,
                            "total_size": size,
                            "sel_size": size,
                            "name": entry.name
                        }
            return node_id
        except PermissionError:
            return None

    def _recalculate_folder_sizes(self, node_id):
        """Calcula de abajo a arriba los tamaños totales y seleccionados."""
        data = self.item_data[node_id]
        if not data["is_dir"]:
            data["sel_size"] = data["file_size"] if data["checked"] else 0
            data["total_size"] = data["file_size"]
            return data["sel_size"], data["total_size"]

        total_s = 0
        selected_s = 0
        for child in self.tree.get_children(node_id):
            c_sel, c_tot = self._recalculate_folder_sizes(child)
            total_s += c_tot
            selected_s += c_sel

        data["total_size"] = total_s
        data["sel_size"] = selected_s
        return selected_s, total_s

    def _refresh_tree_display(self, node_id):
        """Actualiza el texto, iconos de estado y valores de las columnas."""
        data = self.item_data[node_id]
        children = self.tree.get_children(node_id)

        if data["is_dir"]:
            # Determinar si todos, algunos o ningún hijo están marcados
            all_checked = True
            any_checked = False
            for ch in children:
                ch_data = self.item_data[ch]
                if ch_data["checked"]:
                    any_checked = True
                else:
                    all_checked = False

            if not children:
                icon = ICON_CHECKED if data["checked"] else ICON_UNCHECKED
            elif all_checked:
                icon = ICON_CHECKED
                data["checked"] = True
            elif any_checked:
                icon = ICON_PARTIAL
                data["checked"] = True
            else:
                icon = ICON_UNCHECKED
                data["checked"] = False
        else:
            icon = ICON_CHECKED if data["checked"] else ICON_UNCHECKED

        self.tree.item(
            node_id,
            text=f"{icon} {data['name']}",
            values=(format_bytes(data["sel_size"]), format_bytes(data["total_size"]))
        )

        for child in children:
            self._refresh_tree_display(child)

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region not in ("tree", "cell"):
            return

        item_id = self.tree.identify_row(event.y)
        if not item_id or item_id not in self.item_data:
            return

        # Invertir estado
        new_state = not (self.item_data[item_id]["checked"] and self.tree.item(item_id, "text").startswith(ICON_CHECKED))
        self._set_checked_recursive(item_id, new_state)

        # Recalcular todo el árbol y refrescar vista
        for root_node in self.tree.get_children():
            self._recalculate_folder_sizes(root_node)
            self._refresh_tree_display(root_node)

        self.update_stats()

    def _set_checked_recursive(self, item_id, state):
        """Afecta a este elemento y recursivamente a TODOS sus hijos y nietos."""
        self.item_data[item_id]["checked"] = state
        for child_id in self.tree.get_children(item_id):
            self._set_checked_recursive(child_id, state)

    def toggle_all(self, state):
        for root_node in self.tree.get_children():
            self._set_checked_recursive(root_node, state)
            self._recalculate_folder_sizes(root_node)
            self._refresh_tree_display(root_node)
        self.update_stats()

    def update_stats(self):
        total_repo = 0
        total_selected = 0
        file_count = 0

        for d in self.item_data.values():
            if not d["is_dir"]:
                total_repo += d["file_size"]
                if d["checked"]:
                    total_selected += d["file_size"]
                    file_count += 1

        estimated_tokens = int(total_selected / 3.8)

        stats_str = self.t("stats").format(
            files=file_count,
            sel_size=format_bytes(total_selected),
            tot_size=format_bytes(total_repo),
            tokens=estimated_tokens
        )
        self.stats_label.config(text=stats_str)

    def on_tree_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id or item_id not in self.item_data:
            return

        data = self.item_data[item_id]
        if data["is_dir"]:
            return

        # Visor de código
        preview = tk.Toplevel(self.root)
        preview.title(self.t("preview_title").format(file=data["rel_path"]))
        preview.geometry("700x520")

        txt = tk.Text(preview, wrap="none", font=("Consolas", 10), padx=8, pady=8)
        txt.pack(fill=tk.BOTH, expand=True)

        content = self.read_file_safe(data["path"])
        txt.insert("1.0", content)
        txt.config(state="disabled")

    def filter_tree(self, *args):
        query = self.search_var.get().lower().strip()

        def match_node(node_id):
            data = self.item_data[node_id]
            name = data["name"].lower()
            children = self.tree.get_children(node_id)
            child_matched = any(match_node(c) for c in children)
            matches = (query in name) or child_matched or (query == "")
            if matches and query:
                self.tree.item(node_id, open=True)
            return matches

        for root_id in self.tree.get_children():
            match_node(root_id)

    def read_file_safe(self, filepath):
        for enc in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    content = f.read()
                    if '\0' in content:
                        return "[Binary content omitted]"
                    return content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                return f"[Read error: {e}]"
        return "[Decoding error]"

    def generate_ascii_tree(self, selected_files):
        tree_dict = {}
        for rel_path in selected_files:
            parts = rel_path.replace("\\", "/").split("/")
            curr = tree_dict
            for p in parts:
                curr = curr.setdefault(p, {})

        lines = [self.t("tree_header"), "."]

        def _build(d, prefix=""):
            keys = sorted(d.keys())
            for i, k in enumerate(keys):
                is_last = (i == len(keys) - 1)
                lines.append(f"{prefix}{'└── ' if is_last else '├── '}{k}")
                _build(d[k], prefix + ("    " if is_last else "│   "))

        _build(tree_dict)
        return "\n".join(lines) + "\n\n" + "=" * 70 + "\n\n"

    def process_files(self):
        if not self.target_dir or not os.path.isdir(self.target_dir):
            messagebox.showerror("Error", self.t("err_dir"))
            return

        out_name = self.out_name_entry.get().strip()
        if not out_name.endswith(".txt"):
            out_name += ".txt"

        out_path = os.path.join(self.target_dir, out_name)

        selected = [
            (d["path"], d["rel_path"], d["file_size"]) for d in self.item_data.values() 
            if not d["is_dir"] and d["checked"]
        ]

        if not selected:
            messagebox.showwarning("AIPacker Pro", self.t("err_no_files"))
            return

        # Priorizar archivos principales
        priority = ['pubspec.yaml', 'main.dart', 'package.json', 'index.html', 'app.py', 'main.py']
        selected.sort(key=lambda x: (0 if os.path.basename(x[0]).lower() in priority else 1, x[1].lower()))

        try:
            self.status_var.set(self.t("status_loading"))
            self.root.update_idletasks()

            rel_paths = [s[1] for s in selected]
            output_parts = [self.generate_ascii_tree(rel_paths)]

            for full_path, rel_path, _ in selected:
                clean_rel = rel_path.replace("\\", "/")
                ext = os.path.splitext(clean_rel)[1].replace(".", "") or "txt"

                output_parts.append(
                    f"================================================================================\n"
                    f"{self.t('file_header').format(path=clean_rel)}\n"
                    f"================================================================================\n"
                    f"```{ext}\n"
                    f"{self.read_file_safe(full_path)}\n"
                    f"```\n\n"
                )

            final_text = "".join(output_parts)
            with open(out_path, 'w', encoding='utf-8') as out:
                out.write(final_text)

            self.last_generated_content = final_text
            self.last_generated_file = out_path
            self.btn_copy.config(state="normal")

            msg = self.t("status_success").format(file=out_name)
            self.status_var.set(msg)

            # Siguiente nombre en la caja
            self.out_name_entry.delete(0, tk.END)
            self.out_name_entry.insert(0, self.get_next_output_filename(self.target_dir))

            # Mostrar ventana modal detallada
            total_size_bytes = os.path.getsize(out_path)
            self.show_success_modal(out_name, out_path, len(selected), total_size_bytes)

        except Exception as e:
            messagebox.showerror("Error", f"Error:\n{e}")
            self.status_var.set("Error.")

    def show_success_modal(self, filename, filepath, file_count, total_bytes):
        """Ventana modal espaciosa y completa con botones de acción rápida."""
        modal = tk.Toplevel(self.root)
        modal.title(self.t("modal_title"))
        modal.geometry("560x360")
        modal.transient(self.root)
        modal.grab_set()

        content = ttk.Frame(modal, padding=20)
        content.pack(fill=tk.BOTH, expand=True)

        ttk.Label(content, text="🎉 " + self.t("modal_heading"), font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        info_text = self.t("modal_info").format(
            name=filename,
            count=file_count,
            size=format_bytes(total_bytes),
            tokens=int(total_bytes / 3.8),
            path=filepath
        )
        info_label = ttk.Label(content, text=info_text, justify="left", font=("Segoe UI", 9))
        info_label.pack(fill=tk.BOTH, expand=True, pady=5)

        # Botones de Acción
        btn_box = ttk.Frame(content)
        btn_box.pack(fill=tk.X, pady=(15, 0))

        def open_file():
            if sys.platform.startswith('win'):
                os.startfile(filepath)
            elif sys.platform == 'darwin':
                subprocess.run(['open', filepath])
            else:
                subprocess.run(['xdg-open', filepath])

        def open_folder():
            folder = os.path.dirname(filepath)
            if sys.platform.startswith('win'):
                subprocess.run(['explorer', '/select,', os.path.normpath(filepath)])
            elif sys.platform == 'darwin':
                subprocess.run(['open', '-R', filepath])
            else:
                subprocess.run(['xdg-open', folder])

        def copy_and_notify():
            self.copy_to_clipboard()
            modal.destroy()

        ttk.Button(btn_box, text=self.t("btn_open_file"), command=open_file).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_box, text=self.t("btn_open_folder"), command=open_folder).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_box, text=self.t("btn_modal_copy"), command=copy_and_notify).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_box, text=self.t("btn_close"), command=modal.destroy).pack(side=tk.RIGHT, padx=3)

    def copy_to_clipboard(self):
        if self.last_generated_content:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.last_generated_content)
            messagebox.showinfo("AIPacker Pro", self.t("copied"))

def main():
    cli_arg = sys.argv[1] if len(sys.argv) > 1 else None
    root = tk.Tk()
    app = AIPackerApp(root, cli_arg)
    root.mainloop()

if __name__ == "__main__":
    main()