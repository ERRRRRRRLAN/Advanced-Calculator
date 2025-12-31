import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QTextEdit, QLabel, QGridLayout
)
# --- TAMBAHKAN DUA LINE IMPORT INI ---
from PyQt6.QtCore import QRegularExpression, Qt
from PyQt6.QtGui import QRegularExpressionValidator
# -------------------------------------

from core.engine import MathEngine
from core.state_manager import StateManager
from ui.plotter import PlotWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Calculator")
        self.setFixedSize(1000, 700) 
        
        self.engine = MathEngine()
        self.state = StateManager()
        
        self.setup_ui()
        
        # --- TAMBAHKAN BARIS INI ---
        # Memastikan data dari file dimuat ke dalam QTextEdit saat start
        self.update_history_ui() 
        # ---------------------------

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            /* Kustomisasi Textbox yang Lebih Bagus */
            QLineEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 12px;
                padding: 15px;
                font-size: 20px;
                font-family: 'Segoe UI', sans-serif;
                selection-background-color: #2ecc71;
                margin-bottom: 10px;
            }
            QLineEdit {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    border: 1px solid #333333; /* Border tetap sama meski sedang mengetik */
                    border-radius: 12px;
                    padding: 15px;
                    font-size: 20px;
                }
            /* Styling History & Tombol lainnya */
            QTextEdit {
                background-color: #1a1a1a;
                color: #2ecc71;
                border: 1px solid #333333;
                border-radius: 12px;
                font-family: 'Consolas', monospace;
                padding: 10px;
            }
            QPushButton {
                background-color: #2a2a2a;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #353535;
            }
            QPushButton:pressed {
                background-color: #202020;
                padding-top: 2px;
                padding-left: 2px;
            }
            QPushButton#calc_btn {
                background-color: #2ecc71;
                color: #000000;
            }
            QPushButton#calc_btn:hover {
                background-color: #27ae60;
            }
            QLabel {
                color: #666666;
                font-weight: bold;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
        """)

        left_panel = QVBoxLayout()
        
        # Textbox Utama (Tanpa Label di atasnya)
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your equation here...")
        
        # Pastikan bisa fokus dan tidak ReadOnly
        self.input_field.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        regex = QRegularExpression(r"[0-9xXyY\.\+\-\*\/\^\(\)\=\s]*")
        validator = QRegularExpressionValidator(regex, self.input_field)
        self.input_field.setValidator(validator)
        self.input_field.returnPressed.connect(self.on_calculate)
        
        # Numpad & Buttons
        numpad_layout = QGridLayout()
        numpad_layout.setSpacing(8)
        buttons = [
            '7', '8', '9', '/', 'sin',
            '4', '5', '6', '*', 'cos',
            '1', '2', '3', '-', 'tan',
            '0', '.', 'C', '+', 'x',
            'y', '(', ')', '^', '='
        ]
        
        row, col = 0, 0
        for btn_text in buttons:
            btn = QPushButton(btn_text)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setFixedSize(60, 45)
            btn.clicked.connect(lambda checked, ch=btn_text: self.on_button_click(ch))
            # Tambahkan warna khusus untuk operator di samping angka
            if not btn_text.isdigit() and btn_text != '.':
                btn.setStyleSheet("color: #2ecc71; font-size: 16px;")
            numpad_layout.addWidget(btn, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        # Tambahkan Widget ke Layout
        left_panel.addWidget(self.input_field) # Langsung input field tanpa QLabel "Input Command"
        left_panel.addLayout(numpad_layout)
        left_panel.addSpacing(15)
        
        self.calc_btn = QPushButton("EXECUTE")
        self.calc_btn.setObjectName("calc_btn")
        self.calc_btn.setFixedHeight(55)
        self.calc_btn.clicked.connect(self.on_calculate)
        left_panel.addWidget(self.calc_btn)
        
        left_panel.addSpacing(20)
        left_panel.addWidget(QLabel("History Log"))
        self.history_display = QTextEdit()
        left_panel.addWidget(self.history_display)
        
        self.clear_history_btn = QPushButton("Clear History")
        self.clear_history_btn.setFixedHeight(35)
        self.clear_history_btn.setStyleSheet("background-color: #331111; color: #ff5555; border: 1px solid #442222;")
        self.clear_history_btn.clicked.connect(self.on_clear_history)
        left_panel.addWidget(self.clear_history_btn)

        # Plot Panel
        self.plot_widget = PlotWidget()
        self.plot_widget.figure.set_facecolor('#121212')
        self.plot_widget.ax.set_facecolor('#1a1a1a')
        
        main_layout.addLayout(left_panel, 1)
        main_layout.addWidget(self.plot_widget, 2)

    def on_button_click(self, char):
        if char == 'C':
            self.input_field.clear()
        else:
            self.input_field.setText(self.input_field.text() + char)

    def on_calculate(self):
        expr = self.input_field.text().strip()
        
        # 1. Validasi Input Kosong
        if not expr:
            return

        try:
            if 'x' in expr.lower() or 'y' in expr.lower():
                plot_data = self.engine.get_plot_data(expr)
                self.plot_widget.plot_data(plot_data, title=f"Graph: {expr}")
                res = "Graph Plotted"
                self.state.add_to_history(expr, res)
            else:
                res = self.engine.evaluate(expr)
                # Jika hasil mengandung kata "Error"
                if "Error" in str(res):
                    self.history_display.append(f"<span style='color: #e74c3c;'>{expr} -> {res}</span>")
                    return
                self.state.add_to_history(expr, res)
            
            self.update_history_ui()
        except Exception as e:
            # Menampilkan pesan error yang ramah di UI
            error_msg = str(e).split(':')[-1] # Ambil pesan intinya saja
            self.history_display.append(f"<span style='color: #e74c3c;'>Error: {error_msg}</span>")

    def update_history_ui(self):
        self.history_display.clear()
        for item in self.state.get_history():
            self.history_display.append(f"{item['expression']} = {item['result']}")

    def on_clear_history(self):
        self.state.clear_history()
        self.update_history_ui()
    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()

        # 1. PAKSA FOKUS KE TEXTBOX
        # Setiap kali ada tombol ditekan, pastikan input_field yang memegang kendali
        if not self.input_field.hasFocus():
            self.input_field.setFocus()

        # 2. HANDLER KHUSUS NAVIGASI (PANAH KANAN/KIRI)
        # Kita cegah sistem navigasi Qt (select button) dengan memprosesnya manual
        if key in (Qt.Key.Key_Left, Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down, 
                  Qt.Key.Key_Home, Qt.Key.Key_End):
            
            # Kirim event ini langsung ke input_field, jangan biarkan MainWindow memprosesnya
            self.input_field.event(event) 
            event.accept()
            return

        # 3. MAPPING TOMBOL (Sama seperti sebelumnya)
        key_map = {
            Qt.Key.Key_Return: "EXECUTE", 
            Qt.Key.Key_Enter: "EXECUTE", 
            Qt.Key.Key_Escape: "C",       
            ord('*'): "*",
            ord('/'): "/",
            ord('^'): "^",
            ord('('): "(",
            ord(')'): ")",
            ord('='): "=",         
        }

        # 4. Handle Backspace (Gunakan fungsi internal agar posisi kursor akurat)
        if key == Qt.Key.Key_Backspace:
            self.input_field.backspace()
            event.accept()
            return

        # 5. Cari Tombol UI untuk Animasi
        target_text = key_map.get(key, text.lower())
        for btn in self.findChildren(QPushButton):
            if btn.text().lower() == target_text:
                btn.animateClick() 
                event.accept()
                return 

        # 6. Insert Karakter (Angka & Variabel)
        if text and text.lower() in "0123456789.+-*/^()xy":
            # Menggunakan insert agar teks muncul di posisi kursor saat ini
            self.input_field.insert(text)
            event.accept()
            return

        super().keyPressEvent(event)