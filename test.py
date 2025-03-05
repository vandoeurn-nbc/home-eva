import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from result import ResultWindow
from search_form import PropertyPriceEstimation


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResultWindow(1, 'BKK', 'BKK3', 11.547598, 104.917943, 120, 4, 4)
    window.show()
    sys.exit(app.exec())