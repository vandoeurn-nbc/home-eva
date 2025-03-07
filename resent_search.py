import sys
import json
from math import isclose
from search_database import get_recent_searches, get_search_by_id
from result import ResultWindow
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, 
    QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt

class RecentSearchesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

       
    def initUI(self):
        """Initialize the user interface."""
        self.setWindowTitle("Recent Searches")
        self.setGeometry(100, 100, 1440, 1024)

        layout = QVBoxLayout()

        # Logo
        logo_label = self.create_logo()
        layout.addWidget(logo_label)

        # Title and Subtitle
        title_label, subtitle_label = self.create_labels()
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)

        # Table Widget (Custom Style)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)  # 7 columns
        self.tableWidget.setHorizontalHeaderLabels(["Property Type", "District", "Commune", "Price", "Size", "Bedrooms", "Bathrooms"])
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tableWidget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.setStyleSheet(self.table_style())  # Apply custom styling
        self.tableWidget.cellClicked.connect(self.row_clicked)

        # Adjust column width
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

        self.set_background_image()
        self.load_recent_searches()

    def create_logo(self):
        """Create and return the logo label."""
        logo_label = QLabel(self)
        try:
            logo_pixmap = QPixmap("resource/logo.png")
            logo_pixmap = logo_pixmap.scaled(193, 193, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        except Exception:
            logo_label.setText("Logo not found")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return logo_label

    def create_labels(self):
        """Create and return title and subtitle labels."""
        title_label = QLabel("Recently Searched", self)
        title_label.setFont(QFont("Sora", 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("Your recent search history")
        subtitle_label.setFont(QFont("Arial", 16))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        return title_label, subtitle_label

    def set_background_image(self):
        """Set the background image for the window."""
        palette = QPalette()
        try:
            pixmap = QPixmap("resource/background.png") 
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        except Exception:
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        self.setPalette(palette)

    def load_recent_searches(self):
        """Load recent searches into the table."""
        searches = get_recent_searches()
        self.tableWidget.setRowCount(len(searches))

        for row, search in enumerate(searches):
            search_id, property_type, district, commune, price, size, bedrooms, bathrooms = search
            data_list = [property_type, district, commune, price, f"{size} sqm", str(bedrooms), str(bathrooms)]

            for col, data in enumerate(data_list):
                item = QTableWidgetItem(data)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text
                self.tableWidget.setItem(row, col, item)

                # Store search ID as metadata
                if col == 0:
                    item.setData(Qt.ItemDataRole.UserRole, search_id)

    def row_clicked(self, row, column):
        """Open the result screen when a row is clicked."""
        search_id = self.tableWidget.item(row, 0).data(Qt.ItemDataRole.UserRole)
        search_data = get_search_by_id(search_id)

        if search_data:
            property_type, district, commune, price, size, bedrooms, bathrooms = search_data
            self.resultWindow = ResultWindow(property_type, district, commune, price, size, bedrooms, bathrooms)
            self.resultWindow.show()

    def table_style(self):
        """Return the custom stylesheet for the table."""
        return """
            QTableWidget {
                background-color: #2C2F33;
                color: #FFFFFF;
                font-size: 16px;
                border-radius: 10px;
                gridline-color: #444;
            }
            QTableWidget::item {
                border-bottom: 1px solid #444;
                padding: 10px;
            }
            QHeaderView::section {
                background-color: #23272A;
                color: #FFFFFF;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #5865F2;
                color: #FFFFFF;
            }
        """