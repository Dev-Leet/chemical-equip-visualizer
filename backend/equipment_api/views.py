from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.http import HttpResponse
from .models import Dataset, EquipmentData, DatasetSummary, EquipmentTypeStats
from .serializers import (DatasetListSerializer, DatasetDetailSerializer, 
                          EquipmentTypeStatsSerializer, SummaryResponseSerializer)
from data_processor.csv_parser import CSVParser
from data_processor.analyzer import DataAnalyzer
from data_processor.pdf_generator import PDFReportGenerator

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    file = request.FILES.get('file')
    
    if not file:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not file.name.endswith('.csv'):
        return Response({'error': 'Invalid file format. Only CSV files are allowed.'}, 
                        status=status.HTTP_400_BAD_REQUEST)
    
    if file.size > settings.MAX_UPLOAD_SIZE:
        return Response({'error': f'File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE} bytes.'}, 
                        status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
    
    try:
        parser = CSVParser()
        analyzer = DataAnalyzer()
        
        file_hash = parser.generate_hash(file)
        file.seek(0)
        
        if Dataset.objects.filter(file_hash=file_hash, user=request.user).exists():
            return Response({'error': 'This file has already been uploaded.'}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        df = parser.parse_file(file)
        
        dataset = Dataset.objects.create(
            user=request.user,
            filename=file.name,
            file_hash=file_hash,
            file_size=file.size,
            row_count=len(df)
        )
        
        equipment_list = []
        for _, row in df.iterrows():
            equipment_list.append(EquipmentData(
                dataset=dataset,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            ))
        EquipmentData.objects.bulk_create(equipment_list)
        
        summary_data = analyzer.compute_statistics(df)
        DatasetSummary.objects.create(dataset=dataset, **summary_data)
        
        type_distribution = analyzer.get_type_distribution(df)
        for type_data in type_distribution:
            type_stats = analyzer.get_type_statistics(df, type_data['equipment_type'])
            EquipmentTypeStats.objects.create(
                dataset=dataset,
                equipment_type=type_data['equipment_type'],
                count=type_data['count'],
                percentage=type_data['percentage'],
                **type_stats
            )
        
        return Response({
            'dataset_id': dataset.id,
            'filename': dataset.filename,
            'upload_date': dataset.upload_date,
            'row_count': dataset.row_count,
            'file_size': dataset.file_size,
            'message': 'File uploaded and processed successfully'
        }, status=status.HTTP_201_CREATED)
        
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ REAL ERROR: {e}")
        return Response({'error': 'An error occurred while processing the file.'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_datasets(request):
    active_only = request.query_params.get('active_only', 'true').lower() == 'true'
    
    queryset = Dataset.objects.filter(user=request.user)
    if active_only:
        queryset = queryset.filter(is_active=True)
    
    serializer = DatasetListSerializer(queryset, many=True)
    return Response({
        'count': queryset.count(),
        'results': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        serializer = DatasetDetailSerializer(dataset)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        dataset.delete()
        return Response({'message': 'Dataset deleted successfully'}, status=status.HTTP_200_OK)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        summary = DatasetSummary.objects.get(dataset=dataset)
        type_stats = EquipmentTypeStats.objects.filter(dataset=dataset).order_by('-count')
        
        response_data = {
            'dataset_id': dataset.id,
            'filename': dataset.filename,
            'upload_date': dataset.upload_date,
            'statistics': {
                'total_count': summary.total_count,
                'averages': {
                    'flowrate': float(summary.avg_flowrate) if summary.avg_flowrate else None,
                    'pressure': float(summary.avg_pressure) if summary.avg_pressure else None,
                    'temperature': float(summary.avg_temperature) if summary.avg_temperature else None,
                },
                'ranges': {
                    'flowrate': {
                        'min': float(summary.min_flowrate) if summary.min_flowrate else None,
                        'max': float(summary.max_flowrate) if summary.max_flowrate else None,
                    },
                    'pressure': {
                        'min': float(summary.min_pressure) if summary.min_pressure else None,
                        'max': float(summary.max_pressure) if summary.max_pressure else None,
                    },
                    'temperature': {
                        'min': float(summary.min_temperature) if summary.min_temperature else None,
                        'max': float(summary.max_temperature) if summary.max_temperature else None,
                    },
                }
            },
            'type_distribution': [
                {
                    'equipment_type': stat.equipment_type,
                    'count': stat.count,
                    'percentage': float(stat.percentage),
                    'avg_flowrate': float(stat.avg_flowrate) if stat.avg_flowrate else None,
                    'avg_pressure': float(stat.avg_pressure) if stat.avg_pressure else None,
                    'avg_temperature': float(stat.avg_temperature) if stat.avg_temperature else None,
                }
                for stat in type_stats
            ]
        }
        
        return Response(response_data)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    except DatasetSummary.DoesNotExist:
        return Response({'error': 'Summary not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_type_stats(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        type_stats = EquipmentTypeStats.objects.filter(dataset=dataset).order_by('-count')
        
        response_data = {
            'dataset_id': dataset.id,
            'types': [
                {
                    'equipment_type': stat.equipment_type,
                    'count': stat.count,
                    'percentage': float(stat.percentage)
                }
                for stat in type_stats
            ]
        }
        
        return Response(response_data)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request, dataset_id):
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        generator = PDFReportGenerator()
        pdf_buffer = generator.generate_report(dataset)
        
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset_id}.pdf"'
        return response
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': 'Failed to generate PDF report'}, 
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)