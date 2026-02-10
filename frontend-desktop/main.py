import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from ui.login_dialog import LoginDialog
from utils.config import load_config

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("ChemViz")
    
    config = load_config()
    
    login_dialog = LoginDialog(config)
    if login_dialog.exec_() == LoginDialog.Accepted:
        api_client = login_dialog.api_client
        window = MainWindow(config, api_client)
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()