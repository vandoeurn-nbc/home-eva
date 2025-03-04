
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QProgressDialog
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont, QIntValidator
from PyQt6.QtCore import Qt, QTimer
from result import ResultWindow

class PropertyPriceEstimation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        # Set main layout
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
        title_label = QLabel('Let us know your property details', self)
        title_label.setFont(QFont('Sora', 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        subtitle_label = QLabel("These details will help us generate a more accurate report for your property.")
        subtitle_label.setFont(QFont("Arial", 16))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)
        layout.addSpacing(40)
        
        # Custom StyleSheet
        field_style = """
            QComboBox, QLineEdit {
                background-color: #B8B8B8;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                width: 300px;
            }
            QComboBox {
                min-width: 400px;
                max-width: 400px;
            }
            QLineEdit {
                min-width: 400px;
                max-width: 400px;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: url('resource/end-icon.png');
                width: 14px;
                height: 14px;
                margin-right: 10px;
            }
        """
        self.setStyleSheet(field_style)
        
        # Dropdown fields
        self.typeBox = QComboBox()
        self.typeBox.addItems(["Select type", "House", "Condo/Apartment", "Land"])
        
        self.districtBox = QComboBox()
        
        with open('resource/district.json', 'r') as f:
            district_data = json.load(f)
        
        self.districtBox.addItem("Select your District/Khan")
        for district in district_data:
            self.districtBox.addItem(district['en_name'])
        
        self.communeBox = QComboBox()
        
        with open('resource/commune.json', 'r') as f:
            commune_data = json.load(f)
        
        self.communeBox.addItem("Select your commune/Sangkat")
        
        def update_commune_box():
            selected_district = self.districtBox.currentText()
            self.communeBox.clear()
            self.communeBox.addItem("Select your commune/Sangkat")
            for commune in commune_data:
                if commune['district_slug'] == selected_district.lower().replace(" ", "-"):
                    self.communeBox.addItem(commune['en_name'])
        
        self.districtBox.currentIndexChanged.connect(update_commune_box)
        # Input fields with integer validation
        int_validator = QIntValidator()
        
        # Input fields
        self.sizeInput = QLineEdit()
        self.sizeInput.setPlaceholderText("Land/House size in square meters")
        self.sizeInput.setValidator(int_validator)
        
        self.bedroomsInput = QLineEdit()
        self.bedroomsInput.setPlaceholderText("Number of bedrooms")
        self.bedroomsInput.setValidator(int_validator)
        
        self.bathroomsInput = QLineEdit()
        self.bathroomsInput.setPlaceholderText("Number of bathrooms")
        self.bathroomsInput.setValidator(int_validator)
        
        # Search Button
        self.searchButton = QPushButton("SEARCH")
        self.searchButton.setFont(QFont('Sora', 14))
        self.searchButton.setStyleSheet("""
                background-color: #3094CE; 
                color: white; 
                padding: 10px;
                border-radius: 8px; 
                min-width: 400px; 
                max-width: 400px; 
                font-weight: bold;                       
        """)
        def on_search_click():
        
            property_type = self.typeBox.currentText()
            property_type_mapping = {
                "House": 1,
                "Condo/Apartment": 2,
                "Land": 3
            }
            
            property_type_id = property_type_mapping.get(property_type, None)
            size_value = self.sizeInput.text()
            bedrooms_value = self.bedroomsInput.text()
            bathrooms_value = self.bathroomsInput.text()
            selected_commune = self.communeBox.currentText()
            latitude, longitude = None, None
            
            for commune in commune_data:
                if commune['en_name'] == selected_commune:
                    latitude = commune['map']['x']
                    longitude = commune['map']['y']
                    break
            
            print(f"Selected Property Type ID: {property_type_id}")
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            print(f"Size: {size_value}")
            print(f"Bedrooms: {bedrooms_value}")
            print(f"Bathrooms: {bathrooms_value}")
            
            # Show loading dialog
            loading_dialog = QProgressDialog("Loading...", "Cancel", 0, 100, self)
            loading_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            loading_dialog.setAutoClose(True)
            loading_dialog.setAutoReset(True)
            loading_dialog.show()
            loading_dialog.close()
            # property_type, district, commune, size_value, bedrooms_value, bathrooms_value):
            self.resultWindow = ResultWindow(
                property_type, 
                self.districtBox.currentText(), 
                self.districtBox.currentText(), 
                size_value, 
                bathrooms_value, 
                bathrooms_value)
            self.resultWindow.show()
            self.close()    
        self.searchButton.clicked.connect(on_search_click)
        
    
    
        layout.addWidget(self.typeBox, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.districtBox, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.communeBox, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.sizeInput, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.bedroomsInput, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.bathroomsInput, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.searchButton, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(layout)
        self.setGeometry(100, 100, 1440, 1024)
        
        palette = QPalette()
        try:
            pixmap = QPixmap("resource/background.png") 
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        except Exception as e:
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        self.setPalette(palette)

if __name__ == "__main__":
    app = QApplication([])
    window = PropertyPriceEstimation()
    window.show()
    app.exec()