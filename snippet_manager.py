import sys
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QListWidget, QTextEdit, QPushButton, 
                            QInputDialog, QFileDialog, QLineEdit, QMessageBox,
                            QStatusBar)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
import subprocess
import platform
import zipfile
import glob

"""
Snippet Manager v0.004
A modern, light-themed application for managing code snippets and text notes.

Features:
- Store snippets as individual text files
- Search and filter snippets
- Modern light theme interface
- Persistent settings
- Directory-based storage

Version History:
v0.001 - Initial release with basic functionality
v0.002 - Added status bar, version tracking, and modern icons
v0.003 - Changed to light theme and added exit button
v0.004 - Added default snippets directory in application folder
"""

class SnippetManager(QMainWindow):
    VERSION = "0.004"
    
    def __init__(self):
        super().__init__()
        # Get the directory where the script is located
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.settings_file = os.path.join(self.app_dir, "snippet_settings.json")
        self.snippets_dir = self.load_settings()
        self.init_ui()
        self.load_snippets()
        
    def init_ui(self):
        self.setWindowTitle("Snippet Manager")
        self.setMinimumSize(800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left side (snippet list and controls)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search snippets...")
        self.search_box.textChanged.connect(self.filter_snippets)
        left_layout.addWidget(self.search_box)
        
        # Snippet list
        self.snippet_list = QListWidget()
        self.snippet_list.currentItemChanged.connect(self.load_snippet_content)
        left_layout.addWidget(self.snippet_list)
        
        # Buttons with icons
        button_layout = QHBoxLayout()
        
        self.new_btn = QPushButton()
        self.new_btn.setIcon(QIcon.fromTheme("document-new", QIcon("icons/new.png")))
        self.new_btn.setIconSize(QSize(20, 20))
        self.new_btn.setToolTip("New Snippet")
        self.new_btn.clicked.connect(self.new_snippet)
        
        self.save_btn = QPushButton()
        self.save_btn.setIcon(QIcon.fromTheme("document-save", QIcon("icons/save.png")))
        self.save_btn.setIconSize(QSize(20, 20))
        self.save_btn.setToolTip("Save Snippet")
        self.save_btn.clicked.connect(self.save_snippet)
        
        self.delete_btn = QPushButton()
        self.delete_btn.setIcon(QIcon.fromTheme("edit-delete", QIcon("icons/delete.png")))
        self.delete_btn.setIconSize(QSize(20, 20))
        self.delete_btn.setToolTip("Delete Snippet")
        self.delete_btn.clicked.connect(self.delete_snippet)
        
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QIcon.fromTheme("preferences-system", QIcon("icons/settings.png")))
        self.settings_btn.setIconSize(QSize(20, 20))
        self.settings_btn.setToolTip("Settings")
        self.settings_btn.clicked.connect(self.change_directory)
        
        self.exit_btn = QPushButton()
        self.exit_btn.setIcon(QIcon.fromTheme("application-exit", QIcon("icons/exit.png")))
        self.exit_btn.setIconSize(QSize(20, 20))
        self.exit_btn.setToolTip("Exit Application")
        self.exit_btn.clicked.connect(self.close)
        
        self.save_settings_btn = QPushButton()
        self.save_settings_btn.setIcon(QIcon.fromTheme("document-save", QIcon("icons/save.png")))
        self.save_settings_btn.setIconSize(QSize(20, 20))
        self.save_settings_btn.setToolTip("Save Settings")
        self.save_settings_btn.clicked.connect(self.save_settings_and_update_status)
        
        for btn in [self.new_btn, self.save_btn, self.delete_btn, self.settings_btn, self.exit_btn, self.save_settings_btn]:
            button_layout.addWidget(btn)
            btn.setFixedSize(40, 40)
            
        left_layout.addLayout(button_layout)
        
        # Right side (editor)
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        
        # Add widgets to main layout
        layout.addWidget(left_widget, 1)
        layout.addWidget(self.editor, 2)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"Snippet Manager v{self.VERSION}")
        
        self.apply_styles()
        
    def apply_styles(self):
        style = """
        QMainWindow {
            background-color: #ffffff;
        }
        QWidget {
            background-color: #ffffff;
            color: #333333;
        }
        QListWidget {
            background-color: #f5f5f5;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
        }
        QListWidget::item {
            padding: 8px;
            margin: 2px;
            border-radius: 4px;
        }
        QListWidget::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QListWidget::item:hover {
            background-color: #f5f5f5;
        }
        QTextEdit {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 8px;
        }
        QPushButton {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            padding: 8px 15px;
            border-radius: 8px;
            color: #333333;
        }
        QPushButton:hover {
            background-color: #e3f2fd;
            border: 1px solid #90caf9;
        }
        QPushButton:pressed {
            background-color: #bbdefb;
        }
        QLineEdit {
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 8px;
            color: #333333;
        }
        QLineEdit:focus {
            border: 1px solid #90caf9;
            background-color: #ffffff;
        }
        QStatusBar {
            background-color: #f8f9fa;
            color: #666666;
            border-top: 1px solid #e0e0e0;
        }
        """
        self.setStyleSheet(style)
        
    def load_settings(self):
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                snippets_dir = settings.get('snippets_dir', os.path.join(self.app_dir, 'snippets'))
                # Ensure the snippets directory exists
                os.makedirs(snippets_dir, exist_ok=True)
                return snippets_dir
        except FileNotFoundError:
            # Default to a 'snippets' subdirectory in the application directory
            default_dir = os.path.join(self.app_dir, 'snippets')
            # Create the default directory if it doesn't exist
            os.makedirs(default_dir, exist_ok=True)
            return default_dir
            
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump({'snippets_dir': self.snippets_dir}, f)
            
    def change_directory(self):
        # Open a dialog to select a directory
        directory = QFileDialog.getExistingDirectory(self, "Select Snippets Directory", "")
        
        if directory:
            self.snippets_dir = directory
            self.save_settings()  # Save the new directory to settings
            self.status_bar.showMessage(f"Snippets directory changed to: {self.snippets_dir}", 3000)
        else:
            QMessageBox.warning(self, "Warning", "No directory selected.")
        
    def load_snippets(self):
        self.snippet_list.clear()
        if not self.snippets_dir:
            return
            
        for file in os.listdir(self.snippets_dir):
            if file.endswith('.txt'):
                self.snippet_list.addItem(file[:-4])
                
    def filter_snippets(self):
        search_text = self.search_box.text().lower()
        for i in range(self.snippet_list.count()):
            item = self.snippet_list.item(i)
            item.setHidden(search_text not in item.text().lower())
                
    def new_snippet(self):
        if not self.snippets_dir:
            QMessageBox.warning(self, "Warning", "Please select a snippets directory first.")
            return
            
        name, ok = QInputDialog.getText(self, "New Snippet", "Enter snippet name:")
        if ok and name:
            filename = f"{name}.txt"
            filepath = os.path.join(self.snippets_dir, filename)
            
            if os.path.exists(filepath):
                QMessageBox.warning(self, "Warning", "A snippet with this name already exists.")
                return
                
            with open(filepath, 'w') as f:
                f.write('')
                
            self.load_snippets()
            self.snippet_list.setCurrentRow(self.snippet_list.count() - 1)
            
            # Create a zip backup after adding a new snippet
            self.create_zip_backup()
            
    def load_snippet_content(self):
        current_item = self.snippet_list.currentItem()
        if current_item:
            filepath = os.path.join(self.snippets_dir, f"{current_item.text()}.txt")
            try:
                with open(filepath, 'r') as f:
                    self.editor.setText(f.read())
            except FileNotFoundError:
                self.editor.clear()
        else:
            self.editor.clear()
            
    def save_snippet(self):
        current_item = self.snippet_list.currentItem()
        if current_item:
            filepath = os.path.join(self.snippets_dir, f"{current_item.text()}.txt")
            with open(filepath, 'w') as f:
                f.write(self.editor.toPlainText())
            
            # Update the status bar with the file name and location
            self.status_bar.showMessage(f"Saved {current_item.text()} at {filepath} - Snippet Manager v{self.VERSION}", 3000)
            
            # Create a zip backup after saving the snippet
            self.create_zip_backup()
                
    def delete_snippet(self):
        current_item = self.snippet_list.currentItem()
        if current_item:
            reply = QMessageBox.question(self, "Confirm Delete",
                                         f"Are you sure you want to delete '{current_item.text()}'?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.Yes:
                filepath = os.path.join(self.snippets_dir, f"{current_item.text()}.txt")
                try:
                    os.remove(filepath)  # Delete the file
                    self.snippet_list.takeItem(self.snippet_list.row(current_item))  # Remove item from list
                    self.editor.clear()  # Clear the editor
                    self.status_bar.showMessage(f"Deleted {current_item.text()} - Snippet Manager v{self.VERSION}", 3000)
                except OSError as e:
                    QMessageBox.warning(self, "Error", f"Could not delete file: {str(e)}")

    def save_settings_and_update_status(self):
        self.save_settings()  # Call the existing save_settings method
        self.status_bar.showMessage(f"Settings saved to: {self.settings_file}", 3000)  # Update status bar

    def create_zip_backup(self):
        print("Creating zip backup...")
        backup_dir = os.path.join(self.app_dir, 'backsnip')
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = os.path.join(backup_dir, f"backsnip_{timestamp}.zip")
        print(f"Backup will be saved to: {zip_filename}")
        
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in glob.glob(os.path.join(self.snippets_dir, '*.txt')):
                print(f"Adding {file} to zip...")
                zipf.write(file, os.path.basename(file))
        
        self.manage_zip_backups(backup_dir)
        print("Zip backup created successfully.")

    def manage_zip_backups(self, backup_dir):
        # List all zip files in the backup directory
        zip_files = sorted(glob.glob(os.path.join(backup_dir, '*.zip')), key=os.path.getmtime)
        
        # Keep only the latest 5 zip files
        while len(zip_files) > 5:
            os.remove(zip_files[0])  # Remove the oldest zip file
            zip_files.pop(0)  # Remove it from the list

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for better dark theme compatibility
    window = SnippetManager()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 