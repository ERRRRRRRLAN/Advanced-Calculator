from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotWidget(QWidget):
    """Widget khusus untuk menampilkan grafik fungsi."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Inisialisasi Figure Matplotlib
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_data(self, data, title="Graph"):
        try:
            self.ax.clear()
            x, y, z, is_implicit = data
            
            if is_implicit:
                # Cek jika Z mengandung nilai tak terhingga (inf atau nan)
                import numpy as np
                z = np.nan_to_num(z, nan=0.0, posinf=1e6, neginf=-1e6)
                self.ax.contour(x, y, z, levels=[0], colors='white')
            else:
                # Membatasi sumbu Y agar grafik tidak "hilang" karena nilai terlalu besar
                self.ax.plot(x, y, color='#2ecc71', linewidth=2)
                self.ax.set_ylim([-50, 50]) # Batas default tampilan Y
                
            self.ax.set_title(title, color='white', pad=15)
            self.ax.grid(True, color='#333333', linestyle='--')
            self.canvas.draw()
        except Exception as e:
            print(f"Plot Rendering Error: {e}")