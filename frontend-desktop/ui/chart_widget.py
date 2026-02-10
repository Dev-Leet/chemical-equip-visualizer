from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_type_distribution(self, type_distribution):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        if not type_distribution:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            self.canvas.draw()
            return
        
        types = [item['equipment_type'] for item in type_distribution]
        counts = [item['count'] for item in type_distribution]
        colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0', '#F44336', '#00BCD4']
        
        ax.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)],
               startangle=90)
        ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
        
        self.canvas.draw()