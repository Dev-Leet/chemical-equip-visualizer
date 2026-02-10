from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QTableWidget, QTableWidgetItem, 
                              QLabel, QMessageBox, QFileDialog, QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from .upload_dialog import UploadDialog
from .chart_widget import ChartWidget
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self, config, api_client):
        super().__init__()
        self.config = config
        self.api_client = api_client
        self.current_dataset_id = None
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(100, 100, 
                         int(self.config['APP']['window_width']), 
                         int(self.config['APP']['window_height']))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        toolbar_layout = QHBoxLayout()
        self.upload_btn = QPushButton('📁 Upload CSV')
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #004BA0;
            }
        """)
        
        self.export_btn = QPushButton('📄 Export PDF')
        self.export_btn.clicked.connect(self.export_pdf)
        self.export_btn.setEnabled(False)
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6F00;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #E65100;
            }
            QPushButton:disabled {
                background-color: #E0E0E0;
                color: #BDBDBD;
            }
        """)
        
        self.refresh_btn = QPushButton('🔄 Refresh')
        self.refresh_btn.clicked.connect(self.load_datasets)
        
        toolbar_layout.addWidget(self.upload_btn)
        toolbar_layout.addWidget(self.export_btn)
        toolbar_layout.addWidget(self.refresh_btn)
        toolbar_layout.addStretch()
        
        main_layout.addLayout(toolbar_layout)
        
        self.summary_layout = QHBoxLayout()
        self.summary_labels = {}
        for metric in ['Total', 'Avg Temp', 'Avg Pressure', 'Avg Flowrate']:
            card = QWidget()
            card.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border-radius: 8px;
                    padding: 16px;
                }
            """)
            card_layout = QVBoxLayout(card)
            
            label = QLabel('0')
            label.setStyleSheet('font-size: 24px; font-weight: bold;')
            label.setAlignment(Qt.AlignCenter)
            
            title = QLabel(metric)
            title.setStyleSheet('font-size: 12px; color: #757575;')
            title.setAlignment(Qt.AlignCenter)
            
            card_layout.addWidget(label)
            card_layout.addWidget(title)
            
            self.summary_labels[metric] = label
            self.summary_layout.addWidget(card)
        
        main_layout.addLayout(self.summary_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #E0E0E0;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #F5F5F5;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(self.table)
        
        self.chart_widget = ChartWidget()
        main_layout.addWidget(self.chart_widget)
        
        self.datasets_label = QLabel('Recent Uploads:')
        self.datasets_label.setStyleSheet('font-size: 16px; font-weight: bold; margin-top: 16px;')
        main_layout.addWidget(self.datasets_label)
        
        self.datasets_table = QTableWidget()
        self.datasets_table.setColumnCount(4)
        self.datasets_table.setHorizontalHeaderLabels(['Filename', 'Date', 'Rows', 'Action'])
        self.datasets_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.datasets_table.setMaximumHeight(200)
        self.datasets_table.cellClicked.connect(self.on_dataset_clicked)
        main_layout.addWidget(self.datasets_table)
        
        self.statusBar().showMessage('Ready')
    
    def upload_file(self):
        dialog = UploadDialog(self.api_client, self)
        if dialog.exec_():
            self.load_datasets()
            if dialog.dataset_id:
                self.load_dataset(dialog.dataset_id)
    
    def load_datasets(self):
        try:
            response = self.api_client.list_datasets()
            datasets = response['results']
            
            self.datasets_table.setRowCount(len(datasets))
            for row, dataset in enumerate(datasets):
                self.datasets_table.setItem(row, 0, QTableWidgetItem(dataset['filename']))
                self.datasets_table.setItem(row, 1, QTableWidgetItem(dataset['upload_date'][:10]))
                self.datasets_table.setItem(row, 2, QTableWidgetItem(str(dataset['row_count'])))
                
                load_btn = QPushButton('Load')
                load_btn.clicked.connect(lambda checked, did=dataset['id']: self.load_dataset(did))
                self.datasets_table.setCellWidget(row, 3, load_btn)
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load datasets: {str(e)}')
    
    def on_dataset_clicked(self, row, col):
        if col < 3:
            try:
                datasets = self.api_client.list_datasets()['results']
                if row < len(datasets):
                    self.load_dataset(datasets[row]['id'])
            except Exception as e:
                QMessageBox.critical(self, 'Error', str(e))
    
    def load_dataset(self, dataset_id):
        try:
            self.statusBar().showMessage('Loading dataset...')
            self.current_dataset_id = dataset_id
            
            dataset = self.api_client.get_dataset(dataset_id)
            summary = self.api_client.get_summary(dataset_id)
            
            self.update_summary(summary)
            self.update_table(dataset['equipment'])
            self.update_charts(summary)
            
            self.export_btn.setEnabled(True)
            self.statusBar().showMessage('Dataset loaded successfully')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset: {str(e)}')
            self.statusBar().showMessage('Error loading dataset')
    
    def update_summary(self, summary):
        stats = summary['statistics']
        self.summary_labels['Total'].setText(str(stats['total_count']))
        self.summary_labels['Avg Temp'].setText(f"{stats['averages']['temperature']:.1f}°C" if stats['averages']['temperature'] else 'N/A')
        self.summary_labels['Avg Pressure'].setText(f"{stats['averages']['pressure']:.1f} bar" if stats['averages']['pressure'] else 'N/A')
        self.summary_labels['Avg Flowrate'].setText(f"{stats['averages']['flowrate']:.1f} L/m" if stats['averages']['flowrate'] else 'N/A')
    
    def update_table(self, equipment):
        self.table.setRowCount(len(equipment))
        for row, item in enumerate(equipment):
            self.table.setItem(row, 0, QTableWidgetItem(item['equipment_name']))
            self.table.setItem(row, 1, QTableWidgetItem(item['equipment_type']))
            self.table.setItem(row, 2, QTableWidgetItem(str(item['flowrate'])))
            self.table.setItem(row, 3, QTableWidgetItem(str(item['pressure'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(item['temperature'])))
    
    def update_charts(self, summary):
        self.chart_widget.plot_type_distribution(summary['type_distribution'])
    
    def export_pdf(self):
        if not self.current_dataset_id:
            return
        
        try:
            filename, _ = QFileDialog.getSaveFileName(self, 'Save PDF', '', 'PDF Files (*.pdf)')
            if filename:
                pdf_data = self.api_client.get_pdf_report(self.current_dataset_id)
                with open(filename, 'wb') as f:
                    f.write(pdf_data)
                QMessageBox.information(self, 'Success', 'PDF exported successfully')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to export PDF: {str(e)}')