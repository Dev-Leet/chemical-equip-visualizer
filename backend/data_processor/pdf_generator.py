from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from equipment_api.models import DatasetSummary, EquipmentTypeStats, EquipmentData

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1976D2'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1976D2'),
            spaceAfter=12,
        )
    
    def generate_report(self, dataset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        elements = []
        
        elements.append(Paragraph("Equipment Analysis Report", self.title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        elements.extend(self._create_overview_section(dataset))
        elements.extend(self._create_statistics_section(dataset))
        elements.extend(self._create_type_distribution_section(dataset))
        elements.extend(self._create_equipment_table_section(dataset))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def _create_overview_section(self, dataset):
        elements = []
        elements.append(Paragraph("Dataset Overview", self.heading_style))
        
        data = [
            ['Filename:', dataset.filename],
            ['Upload Date:', dataset.upload_date.strftime('%Y-%m-%d %H:%M:%S')],
            ['Total Equipment:', str(dataset.row_count)],
            ['File Size:', f'{dataset.file_size} bytes'],
        ]
        
        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        return elements
    
    def _create_statistics_section(self, dataset):
        elements = []
        elements.append(Paragraph("Statistical Summary", self.heading_style))
        
        try:
            summary = DatasetSummary.objects.get(dataset=dataset)
            
            data = [
                ['Metric', 'Average', 'Minimum', 'Maximum'],
                ['Flowrate (L/min)', 
                 f'{summary.avg_flowrate:.2f}' if summary.avg_flowrate else 'N/A',
                 f'{summary.min_flowrate:.2f}' if summary.min_flowrate else 'N/A',
                 f'{summary.max_flowrate:.2f}' if summary.max_flowrate else 'N/A'],
                ['Pressure (bar)', 
                 f'{summary.avg_pressure:.2f}' if summary.avg_pressure else 'N/A',
                 f'{summary.min_pressure:.2f}' if summary.min_pressure else 'N/A',
                 f'{summary.max_pressure:.2f}' if summary.max_pressure else 'N/A'],
                ['Temperature (°C)', 
                 f'{summary.avg_temperature:.2f}' if summary.avg_temperature else 'N/A',
                 f'{summary.min_temperature:.2f}' if summary.min_temperature else 'N/A',
                 f'{summary.max_temperature:.2f}' if summary.max_temperature else 'N/A'],
            ]
            
            table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ]))
            
            elements.append(table)
        except DatasetSummary.DoesNotExist:
            elements.append(Paragraph("No summary data available", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        return elements
    
    def _create_type_distribution_section(self, dataset):
        elements = []
        elements.append(Paragraph("Equipment Type Distribution", self.heading_style))
        
        type_stats = EquipmentTypeStats.objects.filter(dataset=dataset).order_by('-count')
        
        if type_stats.exists():
            data = [['Equipment Type', 'Count', 'Percentage']]
            for stat in type_stats:
                data.append([stat.equipment_type, str(stat.count), f'{stat.percentage:.2f}%'])
            
            table = Table(data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No type distribution data available", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        return elements
    
    def _create_equipment_table_section(self, dataset):
        elements = []
        elements.append(Paragraph("Equipment Details", self.heading_style))
        
        equipment = EquipmentData.objects.filter(dataset=dataset)[:20]
        
        if equipment.exists():
            data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
            for eq in equipment:
                data.append([
                    eq.equipment_name,
                    eq.equipment_type,
                    f'{eq.flowrate:.2f}' if eq.flowrate else 'N/A',
                    f'{eq.pressure:.2f}' if eq.pressure else 'N/A',
                    f'{eq.temperature:.2f}' if eq.temperature else 'N/A'
                ])
            
            table = Table(data, colWidths=[1.5*inch, 1.3*inch, 1.2*inch, 1.2*inch, 1.3*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1976D2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ]))
            
            elements.append(table)
            
            if EquipmentData.objects.filter(dataset=dataset).count() > 20:
                elements.append(Spacer(1, 0.1*inch))
                elements.append(Paragraph(f"Showing first 20 of {dataset.row_count} equipment entries", 
                                          self.styles['Normal']))
        else:
            elements.append(Paragraph("No equipment data available", self.styles['Normal']))
        
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                  self.styles['Normal']))
        
        return elements