import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QProgressDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QFont, QIntValidator
from PyQt6.QtCore import Qt
from model import estimate_price
from result import ResultWindow

class PropertyPriceEstimation(QWidget):
    def __init__(self):
        super().__init__()
        self.load_data()
        self.initUI()
    
    def load_data(self):
        with open('resource/district.json', 'r') as f:
            self.district_data = json.load(f)
        
        with open('resource/commune.json', 'r') as f:
            self.commune_data = json.load(f)

    def initUI(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo
        logo_label = self.create_logo()
        layout.addWidget(logo_label)
        
        layout.addSpacing(40)
        
        # Title and subtitle
        title_label, subtitle_label = self.create_labels()
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(40)
        
        # Input field styling
        self.setStyleSheet(self.field_style())
        
        # Dropdown fields
        self.typeBox = self.create_combo_box(["Select type", "House", "Condo/Apartment", "Land"], self.update_fields_visibility)
        self.districtBox = self.create_district_combo_box()
        self.communeBox = self.create_commune_combo_box()
        
        # Input fields with integer validation
        self.sizeInput, self.bedroomsInput, self.bathroomsInput = self.create_input_fields()
        
        # Search Button
        self.searchButton = self.create_search_button()
        
        # Add widgets to layout
        self.add_widgets_to_layout(layout)
        
        self.setLayout(layout)
        self.setGeometry(100, 100, 1440, 1024)
        self.set_background_image()

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
        title_label = QLabel('Let us know your property details', self)
        title_label.setFont(QFont('Sora', 32, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        subtitle_label = QLabel("These details will help us generate a more accurate report for your property.")
        subtitle_label.setFont(QFont("Arial", 16))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        return title_label, subtitle_label

    def field_style(self):
        """Return the stylesheet for input fields."""
        return """
            QComboBox, QLineEdit {
                background-color: #3A3A3C;  
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

    def create_combo_box(self, items, on_change_callback=None):
        """Create and return a combo box with the specified items."""
        combo_box = QComboBox()
        combo_box.addItems(items)
        if on_change_callback:
            combo_box.currentIndexChanged.connect(on_change_callback)
        return combo_box

    def create_district_combo_box(self):
        """Create and return the district combo box."""
        district_combo_box = self.create_combo_box(["Select your District/Khan"], None)
        for district in self.district_data:
            district_combo_box.addItem(district['en_name'])
        return district_combo_box

    def create_commune_combo_box(self):
        """Create and return the commune combo box."""
        commune_combo_box = self.create_combo_box(["Select your commune/Sangkat"], None)
        self.districtBox.currentIndexChanged.connect(self.update_commune_box)
        return commune_combo_box

    def create_input_fields(self):
        """Create and return input fields for size, bedrooms, and bathrooms."""
        int_validator = QIntValidator()

        size_input = QLineEdit()
        size_input.setPlaceholderText("Land/House size in square meters")
        size_input.setValidator(int_validator)
        
        bedrooms_input = QLineEdit()
        bedrooms_input.setPlaceholderText("Number of bedrooms")
        bedrooms_input.setValidator(int_validator)
        
        bathrooms_input = QLineEdit()
        bathrooms_input.setPlaceholderText("Number of bathrooms")
        bathrooms_input.setValidator(int_validator)

        return size_input, bedrooms_input, bathrooms_input

    def create_search_button(self):
        """Create and return the search button."""
        search_button = QPushButton("SEARCH")
        search_button.setFont(QFont('Sora', 14))
        search_button.setStyleSheet("""
            background-color: #3094CE; 
            color: white; 
            padding: 10px;
            border-radius: 8px; 
            min-width: 400px; 
            max-width: 400px; 
            font-weight: bold;
        """)
        search_button.clicked.connect(self.on_search_click)
        return search_button

    def add_widgets_to_layout(self, layout):
        """Add all widgets to the layout."""
        layout.addWidget(self.typeBox, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.districtBox, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.communeBox, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.sizeInput, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.bedroomsInput, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.bathroomsInput, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.searchButton, alignment=Qt.AlignmentFlag.AlignHCenter)

    def set_background_image(self):
        """Set the background image for the window."""
        palette = QPalette()
        try:
            pixmap = QPixmap("resource/background.png") 
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        except Exception:
            palette.setColor(QPalette.ColorRole.Window, Qt.GlobalColor.white)
        self.setPalette(palette)

    def on_search_click(self):
    
        # Validate property type selection
        property_type = self.typeBox.currentText()
        property_type_mapping = {
            "House": 1,
            "Condo/Apartment": 2,
            "Land": 3
        }
        property_type_id = property_type_mapping.get(property_type, None)
        if not property_type_id:
            self.show_error_message("Please select a property type.")
            return
        # Validate commune selection
        selected_commune = self.communeBox.currentText()
        if selected_commune == "Select your commune/Sangkat":
            self.show_error_message("Please select your commune.")
            return


        # Validate size input
        size_value = self.sizeInput.text().strip()
        if not size_value:
            self.show_error_message("Please enter the property size in square meters.")
            return
        try:
            size_value = float(size_value)
            if size_value <= 0:
                raise ValueError
        except ValueError:
            self.show_error_message("Please enter a valid number for the property size.")
            return

        # Validate number of bedrooms (optional but if entered, must be a valid integer)
        bedrooms_value = self.bedroomsInput.text().strip()
        if bedrooms_value:
            try:
                bedrooms_value = int(bedrooms_value)
                if bedrooms_value < 0:
                    raise ValueError  # Ensure it is a non-negative integer
            except ValueError:
                self.show_error_message("Please enter a valid number for the number of bedrooms.")
                return
        else:
            bedrooms_value = 0  # Default to 0 if left empty

        # Validate number of bathrooms (optional but if entered, must be a valid integer)
        bathrooms_value = self.bathroomsInput.text().strip()
        if bathrooms_value:
            try:
                bathrooms_value = int(bathrooms_value)
                if bathrooms_value < 0:
                    raise ValueError  # Ensure it is a non-negative integer
            except ValueError:
                self.show_error_message("Please enter a valid number for the number of bathrooms.")
                return
        else:
            bathrooms_value = 0  # Default to 0 if left empty

        # Find the coordinates (latitude, longitude) for the selected commune
        latitude, longitude = None, None
        for commune in self.commune_data:
            if commune['en_name'] == selected_commune:
                latitude = commune['map']['x']
                longitude = commune['map']['y']
                break
        
        # Check if commune coordinates are found
        if latitude is None or longitude is None:
            self.show_error_message("Commune data not found.")
            return

        # Estimate the price
        price = estimate_price(property_type_id, latitude, longitude, size_value, bedrooms_value, bathrooms_value)

        # Show loading dialog
        loading_dialog = QProgressDialog("Loading...", "Cancel", 0, 100, self)
        loading_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        loading_dialog.setAutoClose(True)
        loading_dialog.setAutoReset(True)
        loading_dialog.show()
        
        # Close the loading dialog once the price is calculated
        loading_dialog.close()

        # Show the result window
        self.resultWindow = ResultWindow(
            property_type, 
            self.districtBox.currentText(), 
            self.communeBox.currentText(), 
            price,
            size_value, 
            bedrooms_value, 
            bathrooms_value)
        self.resultWindow.show()


    def update_fields_visibility(self):
        """Update visibility of input fields based on selected property type."""
        property_type = self.typeBox.currentText()
        if property_type == "House":
            self.bedroomsInput.show()
            self.bathroomsInput.show()
        else:
            self.bedroomsInput.hide()
            self.bathroomsInput.hide()

    def update_commune_box(self):
        """Update the commune combo box based on selected district."""
        selected_district = self.districtBox.currentText()
        self.communeBox.clear()
        self.communeBox.addItem("Select your commune/Sangkat")
        for commune in self.commune_data:
            if commune['district_slug'] == selected_district.lower().replace(" ", "-"):
                self.communeBox.addItem(commune['en_name'])

    def show_error_message(self, message):
        """Show an error message in a message box."""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.setWindowTitle("Input Error")
        msg.exec()
