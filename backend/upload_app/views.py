from django.shortcuts import render

# Create your views here.
import os
import random
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.conf import settings
from .utils import process_nsl_kdd_file

def index(request):
    """Vista principal - solo renderiza template"""
    return render(request, 'upload_app/index.html')

def upload_file(request):
    """ BACKEND: Procesa el archivo subido"""
    if request.method == 'POST' and request.FILES.get('dataset_file'):
        uploaded_file = request.FILES['dataset_file']
        
        # Validar tipo de archivo
        allowed_extensions = ['.txt', '.arff']
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_extension not in allowed_extensions:
            return render(request, 'upload_app/index.html', {
                'error': f'Tipo de archivo no permitido. Use: {", ".join(allowed_extensions)}'
            })
        
        # Guardar archivo temporalmente
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_path = fs.path(filename)
        
        try:
            # ✅ BACKEND: Procesar archivo NSL-KDD
            processed_data = process_nsl_kdd_file(file_path)
            
            # Limpiar archivo temporal
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return render(request, 'upload_app/results.html', {
                'data': processed_data,
                'filename': uploaded_file.name,
                'total_records': len(processed_data),
                'sample_percentage': int(settings.SAMPLE_PERCENTAGE * 100)
            })
            
        except Exception as e:
            # Limpiar en caso de error
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return render(request, 'upload_app/index.html', {
                'error': f'Error procesando el archivo NSL-KDD: {str(e)}'
            })
    
    return render(request, 'upload_app/index.html', {
        'error': 'Por favor, selecciona un archivo válido'
    })

def api_file_info(request):
    """ BACKEND: API para información del archivo"""
    return JsonResponse({
        'allowed_extensions': ['.txt', '.arff'],
        'max_file_size': '50MB',
        'sample_percentage': '5%',
        'dataset': 'ISCX NSL-KDD 2009'
    })