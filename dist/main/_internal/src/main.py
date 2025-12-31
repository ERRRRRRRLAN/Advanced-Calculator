import sys
# Menambahkan import yang hilang secara eksplisit
from PyQt6.QtWidgets import QApplication 
from ui.main_window import MainWindow

def main():
    # Inisialisasi aplikasi
    app = QApplication(sys.argv)
    
    # Instance window utama
    window = MainWindow()
    window.resize(1000, 700)
    window.show()
    
    # Loop aplikasi
    sys.exit(app.exec())

if __name__ == "__main__":
    main()