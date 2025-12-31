# 🧮 Advanced Graphing Calculator

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-v6.4+-green?style=for-the-badge&logo=qt)
![Matplotlib](https://img.shields.io/badge/Matplotlib-v3.7+-red?style=for-the-badge&logo=python)

Advanced Graphing Calculator is a desktop application built with Python and PyQt6 that combines scientific calculator functionality with a powerful 2D function plotter. This application is designed to provide an intuitive user experience with a synchronized input system between the physical keyboard and the visual interface.

## ✨ Key Features

* **🚀 Smart Input System**: Advanced `keyPressEvent` handling to synchronize physical keyboard input with on-screen button animations.
* **📈 Dynamic Plotting**: Instant visualization for various mathematical functions (such as `sin`, `cos`, `tan`, and algebraic equations) using Matplotlib integration.
* **🛡️ Robust Error Handling**: Zero-division protection, syntax validation via SymPy, and informative error logs within the UI.
* **📜 Persistent History**: Automatically saves calculation history to a local database (JSON) and reloads it whenever the app is launched.
* **⌨️ Pro Navigation**: Full support for arrow keys for cursor navigation, auto-focus while typing, and calculation execution via the "Enter" key.
* **🎨 Modern UI**: Elegant dark mode interface with customized widgets, smooth hover effects, and a responsive layout.
* **📸 Export Results**: Save generated graphs directly to high-quality image files (.PNG).

## 🛠️ Tech Stack

* **GUI Framework**: PyQt6
* **Math Engine**: SymPy (Symbolic Mathematics)
* **Plotting Library**: Matplotlib
* **Data Handling**: JSON for persistent state management
* **Build Tool**: PyInstaller & Inno Setup

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* Pip (Python package manager)

### Installation
1.  **Clone the repository**
    ```bash
    git clone [https://github.com/username/advanced-calculator.git](https://github.com/username/advanced-calculator.git)
    cd advanced-calculator
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**
    ```bash
    python src/main.py
    ```

## 📦 Building Executable File (.exe)

To generate a standalone `.exe` for Windows using PyInstaller:

```powershell
python -m PyInstaller --noconsole --onedir --icon="app_icon.ico" --add-data "src;src" --paths src src/main.py
```
After the build is complete, use Inno Setup to wrap the dist folder into a professional installer.

## 📂 Project Structure

```
opencoder/
├── core/               # Mathematical logic & history management
├── ui/                 # PyQt6 Window & Plotter components
├── src/
│   └── main.py         # Application entry point
├── requirements.txt    # Project dependency list
└── README.md           # Project documentation
```

## 🤝 Contributing
Contributions are welcome! If you have suggestions for new features or improvements, please:
1. **Fork** this project.
2. Create a **Feature Branch** (git checkout -b feature/AmazingFeature).
3. **Commit** your changes (git commit -m 'Add AmazingFeature').
4. **Push** to the Branch (git push origin feature/AmazingFeature).
5. Open a **Pull Request**.
