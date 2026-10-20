# 📦 AIPacker Pro — AI Context Bundler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D6.svg)](https://www.microsoft.com/windows)

**AIPacker Pro** is a modern, visual, and intuitive desktop utility tailored for developers who use Large Language Models (**LLMs**) such as ChatGPT, Claude 3.5 Sonnet, DeepSeek, Gemini, etc.

It allows you to bundle an entire software project into a single, well-structured, and optimized context text file. It preserves your project's directory hierarchy, formats code blocks with syntax tags, and automatically filters out heavy compilation artifacts and build directories.

---

## 🚀 Key Features

- **Guided 3-Step GUI:** Clear, structured workflow with native high-DPI support on Windows (crisp fonts, no blurriness).
- **True Cascading Recursive Tree Selection:**
  - When loading a project, **every file and subfolder across all depths** is selected by default.
  - Checking or unchecking a folder immediately updates all nested child folders and files recursively.
  - Three visual state indicators: Fully Checked (`☑`), Partially Checked (`▣`), and Unchecked (`☐`).
- **Live Metrics & Token Estimation:**
  - Multi-column tree view displaying **Selected Size** vs. **Total Size** per file and folder.
  - Real-time calculation of package size and an **estimated token count** to prevent context window overflows.
- **Smart Build & Noise Filtering:**
  - Automatically skips bulky build directories and dependency caches: `node_modules`, `build/`, `.dart_tool/`, `target/`, `.gradle/`, `Pods/`, `__pycache__/`, `.git/`, `.venv/`, etc.
  - Automatically parses and respects your local `.gitignore` rules if present.
  - Broad out-of-the-box support for Flutter/Dart, Python, Web (JS/TS/HTML/CSS), C/C++, Rust, Go, Java, Kotlin, Swift, YAML, JSON, config files, and more.
- **Quick Code Previewer:** Double-click any file in the tree to view its source code in a lightweight preview window before exporting.
- **Real-Time Search Filter:** Locate specific files, components, or modules instantly.
- **Full Internationalization (i18n):** Switch dynamically between 6 languages on the fly (no restart required):
  - 🇬🇧 English (*Default*)
  - 🇪🇸 Spanish
  - 🇩🇪 German
  - 🇫🇷 French
  - 🇮🇹 Italian
  - 🇵🇹 Portuguese
- **Session Persistence:** Remembers your preferred language and the last opened directory across restarts (`aipacker_config.json`).
- **Rich Post-Processing Modal:** Once exported, open the output file directly, reveal it in Windows Explorer, or copy the entire bundle straight to your clipboard.
- **Non-Destructive Auto-Increment:** Automatic detection of previous runs (`total_1.txt`, `total_2.txt`, etc.) so work is never overwritten.

---

## 🛠️ Requirements & Installation

### Option 1: Running Directly with Python

1. Clone this repository:
   ```bash
   git clone https://github.com/ferastur3d/aipacker.git
   cd aipacker


=========================================================================================================================================


# 📦 AIPacker Pro — AI Context Bundler

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows-0078D6.svg)](https://www.microsoft.com/windows)

**AIPacker Pro** es una herramienta de escritorio moderna, visual e intuitiva diseñada para desarrolladores que utilizan Modelos de Lenguaje Grande (**LLMs**) como ChatGPT, Claude 3.5 Sonnet, DeepSeek, Gemini, etc. 

Permite empaquetar proyectos completos de software en un único archivo de contexto estructurado, limpio y optimizado, respetando la jerarquía de archivos y omitiendo automáticamente artefactos de compilación innecesarios.

---

## 🚀 Características Principales

- **Interfaz Gráfica Intuitiva (GUI):** Flujo guiado en 3 sencillos pasos, con soporte nativo para monitores de alta resolución (DPI Awareness en Windows).
- **Selección Jerárquica en Cascada:**
  - Al cargar un proyecto, todo el contenido queda marcado por defecto.
  - Al marcar/desmarcar una carpeta, se actualizan recursivamente todas sus subcarpetas y archivos contenidos.
  - Estados visuales dinámicos: Completamente marcado (`☑`), Parcialmente marcado (`▣`) o Desmarcado (`☐`).
- **Métricas y Estimación en Tiempo Real:** 
  - Muestra columnas con el tamaño seleccionado frente al tamaño total por archivo y directorio.
  - Cálculo en vivo del peso total del paquete y **estimación aproximada de Tokens**.
- **Filtro Inteligente de Compilación y Ruido:**
  - Omite automáticamente dependencias y compilaciones pesadas: `node_modules`, `build/`, `.dart_tool/`, `target/`, `.gradle/`, `Pods/`, `__pycache__/`, `.git/`, `.venv/`, etc.
  - Lee y respeta automáticamente las reglas de tu archivo `.gitignore` local si existe.
  - Soporte amplio para proyectos Flutter/Dart, Python, Web (JS/TS/HTML/CSS), Rust, C/C++, Java, Kotlin, Swift, configs YAML, JSON, etc.
- **Previsualizador Rápido:** Haz doble clic en cualquier archivo del árbol para inspeccionar su código antes de empaquetar.
- **Filtro de Búsqueda:** Encuentra archivos o módulos específicos en tiempo real mediante una barra de búsqueda integrada.
- **Multilenguaje (i18n):** Disponible en 6 idiomas con cambio dinámico al instante:
  - 🇬🇧 Inglés (*por defecto*)
  - 🇪🇸 Español
  - 🇩🇪 Alemán
  - 🇫🇷 Francés
  - 🇮🇹 Italiano
  - 🇵🇹 Portugués
- **Persistencia de Sesión:** Recuerda automáticamente el último idioma seleccionado y la última ruta de proyecto trabajada (`aipacker_config.json`).
- **Modal de Resultados Completo:** Tras empaquetar, abre el archivo generado, accede a su carpeta en el Explorador de Windows o copia todo el contenido directamente al portapapeles.
- **Numeración Secuencial:** Detección automática para no sobrescribir salidas (`total_1.txt`, `total_2.txt`, etc.).

---

## 🛠️ Requisitos e Instalación

### Opción 1: Ejecutar directamente con Python

1. Clona el repositorio:
   ```bash
   git clone https://github.com/ferastur3d/aipacker.git
   cd aipacker
