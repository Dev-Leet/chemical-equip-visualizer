from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                              QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from services.api_client import APIClient

class LoginDialog(QDialog):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.api_client = APIClient(config['API']['base_url'])
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Login - Chemical Equipment Visualizer')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        title = QLabel('Chemical Equipment Visualizer')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #1976D2;')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel('Sign in to your account')
        subtitle.setStyleSheet('color: #757575; margin-bottom: 20px;')
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #1976D2;
            }
        """)
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        
        layout.addSpacing(20)
        
        self.login_btn = QPushButton('Sign In')
        self.login_btn.clicked.connect(self.handle_login)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #004BA0;
            }
        """)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            self.api_client.login(username, password)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, 'Login Failed', str(e))