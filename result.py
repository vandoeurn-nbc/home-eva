
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont
from PyQt6.QtCore import Qt

class ResultWindow(QWidget):
    def __init__(self, property_type, district, commune, price, size_value, bedrooms_value, bathrooms_value):
        super().__init__()
        self.initUI(property_type, district, commune, price, size_value, bedrooms_value, bathrooms_value)
    
    def initUI(self, property_type, district, commune, price, size_value, bedrooms_value, bathrooms_value):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        logo_label = QLabel(self)
        try:
            logo_pixmap = QPixmap("resource/logo.png")
            logo_pixmap = logo_pixmap.scaled(193, 193, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pixmap)
        except Exception as e:
            logo_label.setText("Logo not found")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        layout.addSpacing(40)
        
        # Title
        title_label = QLabel('Property result', self)
        title_label.setFont(QFont('Sora', 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        layout.addSpacing(16)
        font = QFont('Arial', 18)

        # Estimated Price
        estimate_price_label = QLabel(f"Estimated Price: {price}")
        estimate_price_label.setFont(QFont('Arial', 24))
        estimate_price_label.setMargin(20)
        estimate_price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(estimate_price_label)
        
        # Display the property details
        property_type_label = QLabel(f"Property Type: {property_type}")
        property_type_label.setFont(font)
        layout.addWidget(property_type_label)
        
        district_label = QLabel(f"District: {district}")
        district_label.setFont(font)
        layout.addWidget(district_label)
        
        commune_label = QLabel(f"Commune: {commune}")
        commune_label.setFont(font)
        layout.addWidget(commune_label)
        
        size_label = QLabel(f"Land/House size: {size_value} sqm")
        size_label.setFont(font)
        layout.addWidget(size_label)
        
        # Only add bedroom & bathroom labels if it's a House
        if property_type == "House":
            bedrooms_label = QLabel(f"Number of bedrooms: {bedrooms_value}")
            bedrooms_label.setFont(font)
            layout.addWidget(bedrooms_label)

            bathrooms_label = QLabel(f"Number of bathrooms: {bathrooms_value}")
            bathrooms_label.setFont(font)
            layout.addWidget(bathrooms_label)

        self.setLayout(layout)
        self.setGeometry(100, 100, 1440, 1024)
        
        # Background
        palette = QPalette()
        try:
            pixmap = QPixmap("resource/background.png") 
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        except Exception as e:
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        self.setPalette(palette)
