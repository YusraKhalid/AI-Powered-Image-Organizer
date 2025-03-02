import sys
import requests
from PyQt6.QtWidgets import QApplication, QLabel, QMessageBox, QPushButton, QVBoxLayout, QWidget, QFileDialog, QCheckBox, QListWidget
from PyQt6.QtGui import QPixmap, QFont, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt
import os
import send2trash

API_URL = "http://127.0.0.1:8000/upload/"

class ImageApp(QWidget):
    def __init__(self):
        super().__init__()

        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap("logo.png") 
        self.logo_label.setPixmap(self.logo_pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.image_paths = []
        self.current_index = 0
        self.categorized_images = {}
        self.view_by_category = False
        self.current_category = None
        self.kept_images = set()  


        # UI Elements
        self.setWindowTitle("🖼️ AI-Powered Image Viewer & Categorizer")
        self.setGeometry(100, 100, 700, 600)
        self.setAcceptDrops(True)  # Enable Drag & Drop
        self.setStyleSheet("background-color: #806294; color: #ECE8ED;")

        self.setStyleSheet("""
            QWidget {
                background-color: #806294; 
                color: #ECE8ED; 
                border: 5px solid #9E76DB; /* Adds a nice border */
                border-radius: 10px; /* Rounded corners */
            }
        """)


        # Image Display
        self.image_label = QLabel("Drag & Drop Images Here", self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.image_label.setStyleSheet("border: 2px dashed #C3B5D6; background-color: #C3B5D6; padding: 10px; border-radius: 8px;")
        # self.image_label.setStyleSheet("""
        #     border: 4px solid #C3B5D6; 
        #     background-color: #C3B5D6; 
        #     padding: 10px;
        #     border-radius: 8px;
        # """)

        self.setStyleSheet("""
            QWidget {
                background-color: #806294;
                color: #ECE8ED;
                border: 5px solid #9E76DB;
                border-radius: 10px;
                background-image: url('background.jpg'); 
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover;
            }
        """)

        self.category_label = QLabel("Category: ", self)
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.category_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        self.count_label = QLabel("Total Images: 0", self)
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Upload Buttons
        self.upload_file_button = QPushButton("📂 Upload Images")
        self.upload_file_button.clicked.connect(self.upload_images)

        self.upload_folder_button = QPushButton("📁 Upload Folder")
        self.upload_folder_button.clicked.connect(self.upload_folder)

        # View by Category Toggle
        self.category_check = QCheckBox("View by Category", self)
        self.category_check.stateChanged.connect(self.toggle_category_view)

        # Category List
        self.category_list = QListWidget(self)
        self.category_list.itemClicked.connect(self.select_category)
        self.category_list.setVisible(False)
        self.category_list.setStyleSheet("background-color: #C3B5D6; border: none; padding: 5px; color: #806294; font-weight: bold;")

        # Action Buttons
        self.delete_button = QPushButton("❌ Delete")
        self.delete_button.clicked.connect(self.delete_image)
        self.delete_button.setEnabled(False)

        self.next_button = QPushButton("🔁 Repeat")
        self.next_button.clicked.connect(self.next_image)
        self.next_button.setEnabled(False)

        # Add Keep Button
        self.keep_button = QPushButton("✅ Keep")
        self.keep_button.clicked.connect(self.keep_image)
        self.keep_button.setEnabled(False)

        for btn in [self.upload_file_button, self.upload_folder_button, self.delete_button, self.next_button, self.keep_button]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #B58EF1;  /* Slightly darker for contrast */
                    color: #fff;
                    border-radius: 8px;
                    font-weight: bold;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #9E76DB;  /* Even darker on hover */
                }
            """)

        # Layout
        layout = QVBoxLayout()
        
        layout.addWidget(self.category_label)
        layout.addWidget(self.count_label)
        layout.addWidget(self.upload_file_button)
        layout.addWidget(self.upload_folder_button)
        layout.addWidget(self.category_check)
        layout.addWidget(self.category_list)
        layout.addWidget(self.logo_label)  
        layout.addWidget(self.image_label)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.next_button)
        layout.addWidget(self.keep_button)

        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):

        """Accept drag event for images even after reset."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):

        """Handle dropped images and restart image processing."""
        files = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg'))]

        if files:
            self.image_paths.extend(files)
            self.display_image()


    def upload_images(self):
        """Upload multiple images manually"""
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg)")

        if files:
            self.image_paths.extend(files)
            self.display_image()

    def upload_folder(self):
        """Uploads all images from a selected folder"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.image_paths.extend([os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            self.display_image()

    def toggle_category_view(self):
        """Toggles category mode and categorizes images if needed"""
        self.view_by_category = self.category_check.isChecked()
        self.current_category = None

        if self.view_by_category:
            self.categorize_images()
            self.category_list.setVisible(True)
            self.image_label.setText("📂 Select a category from the list")
        else:
            self.category_list.setVisible(False)
            self.display_image()

    def categorize_images(self):
        """Categorizes images only when "View by Category" is checked"""
        self.categorized_images = {}

        for img_path in self.image_paths:
            response = self.upload_to_api(img_path)
            category = response.get("category", "Uncategorized")

            if category not in self.categorized_images:
                self.categorized_images[category] = []

            self.categorized_images[category].append(img_path)

        self.update_category_list()

    def delete_image(self):
        """Moves the current image to the Recycle Bin instead of deleting permanently."""
        if self.view_by_category and self.current_category:
            category_images = self.categorized_images.get(self.current_category, [])
            if not category_images:
                return
            img_path = category_images.pop(self.current_index)

            if not category_images:
                del self.categorized_images[self.current_category]  # Remove empty category
                self.update_category_list()

        else:
            if not self.image_paths:
                return
            img_path = self.image_paths.pop(self.current_index)

        try:
            send2trash.send2trash(img_path)  # ✅ Move to Recycle Bin
        except Exception as e:
            print(f"Error moving image to Recycle Bin: {e}")

        self.display_image()


    def upload_to_api(self, image_path):
        """Send image to FastAPI for AI categorization"""
        with open(image_path, "rb") as img_file:
            response = requests.post(API_URL, files={"image": img_file})
        return response.json()

    def select_category(self, item):
        """Handles category selection and displays the first image in it"""
        self.current_category = item.text().split(" (")[0]  
        self.current_index = 0
        self.display_image()

    def update_category_list(self):
        """Updates category list with image counts"""
        self.category_list.clear()
        for category, images in self.categorized_images.items():
            if images:
                self.category_list.addItem(f"{category} ({len(images)})")


    def display_image(self):
        """Displays the current image and resets the app when all images are viewed or kept."""
        
        # Remove kept images from the list
        self.image_paths = [img for img in self.image_paths if img not in self.kept_images]

        # ✅ If all images in category are viewed, show completion dialog
        print(self.categorized_images)
        if self.view_by_category and self.current_category:
            category_images = self.categorized_images.get(self.current_category, [])
            category_images = [img for img in category_images if img not in self.kept_images]

            if not category_images:
                reply = QMessageBox.question(self, "Category Completed", 
                    "All images in this category are viewed. Do you want to check remaining images?", 
                    QMessageBox.StandardButton.Ok)
                
                if reply == QMessageBox.StandardButton.Yes:
                    self.view_by_category = False
                    self.category_check.setChecked(False)
                    self.display_image()
                else:
                    self.image_label.setText("No more images left in this category")
                    self.count_label.setText("")
                return
            
            img_path = category_images[self.current_index % len(category_images)]
            self.count_label.setText(f"Total Images: {len(category_images)}")
            print(f"Category: {category_images}")
            
        
        else:
            # ✅ If all images (including non-categorized) are viewed, reset the app
            if not self.image_paths:
                if self.categorized_images:
                    reply = QMessageBox.question(self, "All Images Completed", 
                        "All images have been viewed or kept. Do you want to restart the app?", 
                        QMessageBox.StandardButton.Ok)

                    if reply == QMessageBox.StandardButton.Ok:
                        self.reset_app()
                    else:
                        self.image_label.setText("No more images left")
                        self.count_label.setText("")
                        self.category_label.setText("")
                else:
                    self.image_label.setText("No Images Left")
                    self.category_label.setText("")
                    self.count_label.setText("")
                    self.delete_button.setEnabled(False)
                    self.next_button.setEnabled(False)
                    self.keep_button.setEnabled(False)
                    self.reset_app()
                return

            img_path = self.image_paths[self.current_index % len(self.image_paths)]
            self.count_label.setText(f"Total Images: {len(self.image_paths)}")

        pixmap = QPixmap(img_path)
        self.image_label.setPixmap(pixmap.scaled(500, 400, Qt.AspectRatioMode.KeepAspectRatio))
        self.category_label.setText(f"Category: {self.current_category if self.view_by_category else 'All Images'}")

        # ✅ Enable buttons when images are available
        self.delete_button.setEnabled(True)
        self.next_button.setEnabled(True)
        self.keep_button.setEnabled(True)

    def reset_app(self):
        print("Resetting the app")
        """Resets the application to its initial state while keeping Drag & Drop enabled."""
        self.image_paths = []
        self.kept_images = set()
        self.categorized_images = {}
        self.current_index = 0
        self.view_by_category = False
        self.current_category = None

        self.category_list.clear()
        self.image_label.setText("Drag & Drop Images Here")
        self.category_label.setText("")
        self.count_label.setText("")
        self.category_check.setChecked(False)

        # ✅ Disable buttons until new images are uploaded
        self.delete_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.keep_button.setEnabled(False)

        # ✅ Re-enable drag & drop functionality
        self.setAcceptDrops(True)


    def next_image(self):
        """Displays the next image properly"""
        if self.view_by_category and self.current_category:
            category_images = self.categorized_images.get(self.current_category, [])
            if not category_images:
                return
            self.current_index = (self.current_index + 1) % len(category_images)
        else:
            if not self.image_paths:
                return
            self.current_index = (self.current_index + 1) % len(self.image_paths)

        self.display_image()


    def keep_image(self):
        """Marks the current image as kept so it won't be displayed again."""
        if self.view_by_category and self.current_category:
            category_images = self.categorized_images.get(self.current_category, [])
            if not category_images:
                return
            img_path = category_images.pop(self.current_index)

            if not category_images:
                del self.categorized_images[self.current_category]
                self.update_category_list()

        else:
            if not self.image_paths or not self.image_paths[self.current_index]:
                return
            img_path = self.image_paths.pop(self.current_index)

        self.kept_images.add(img_path)  # ✅ Add image to kept list
        self.display_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec())

