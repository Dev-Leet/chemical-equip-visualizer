from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                              QFileDialog, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class UploadWorker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path
    
    def run(self):
        try:
            result = self.api_client.upload_csv(self.file_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class UploadDialog(QDialog):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.file_path = None
        self.dataset_id = None
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Upload CSV File')
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout()
        
        title = QLabel('Select CSV File to Upload')
        title.setStyleSheet('font-size: 16px; font-weight: bold;')
        layout.addWidget(title)
        
        self.file_label = QLabel('No file selected')
        self.file_label.setStyleSheet('color: #757575; margin: 10px 0;')
        layout.addWidget(self.file_label)
        
        browse_btn = QPushButton('Browse Files')
        browse_btn.clicked.connect(self.browse_file)
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #1976D2;
                border: 1px solid #1976D2;
                padding: 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #E3F2FD;
            }
        """)
        layout.addWidget(browse_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.upload_btn = QPushButton('Upload')
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004BA0;
            }
            QPushButton:disabled {
                background-color: #E0E0E0;
                color: #BDBDBD;
            }
        """)
        layout.addWidget(self.upload_btn)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        self.setLayout(layout)
    
    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path.split('/')[-1])
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        if not self.file_path:
            return
        
        self.upload_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker = UploadWorker(self.api_client, self.file_path)
        self.worker.finished.connect(self.on_upload_success)
        self.worker.error.connect(self.on_upload_error)
        self.worker.start()
    
    def on_upload_success(self, result):
        self.dataset_id = result['dataset_id']
        self.progress_bar.setValue(100)
        QMessageBox.information(self, 'Success', 'File uploaded successfully')
        self.accept()
    
    def on_upload_error(self, error):
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        QMessageBox.critical(self, 'Error', f'Upload failed: {error}')