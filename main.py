import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from search_form import PropertyPriceEstimation

class BackgroundWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1440, 1024)
        
        palette = QPalette()
        pixmap = QPixmap("resource/background.png") 
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        self.setPalette(palette)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop) 
        
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("resource/logo.png")
        logo_pixmap = logo_pixmap.scaled(193, 193, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        title_label = QLabel('Properties Price Estimation System', self)
        title_label.setFont(QFont('Sora', 54, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        layout.addSpacing(200)
        
        title_label = QLabel('Find out what your home could be worth', self)
        title_label.setFont(QFont('Sora', 32))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        layout.addSpacing(16)
        
        get_start_button = QPushButton('GET STARTED', self)
        get_start_button.setFont(QFont('Sora', 14))
        get_start_button.setStyleSheet("""
            background-color: #3094CE; 
            color: white; 
            min-width: 180px; 
            max-width: 180px;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        """)
        get_start_button.clicked.connect(self.open_form)
        layout.addWidget(get_start_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
    def open_form(self):
        self.form_window = PropertyPriceEstimation()
        self.form_window.show()
        self.close()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BackgroundWindow()
    window.show()
    sys.exit(app.exec())
