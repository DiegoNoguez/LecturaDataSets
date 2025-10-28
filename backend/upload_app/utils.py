import os
import random
from django.conf import settings

def process_nsl_kdd_file(file_path):
    """
    ✅ BACKEND: Lógica específica para procesar archivos NSL-KDD
    Devuelve aproximadamente el 5% de los datos
    """
    data = []
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
            
            # Si el archivo es pequeño, devolver todo
            if len(lines) <= 20:
                return [line.strip() for line in lines if line.strip()]
            
            # Calcular muestra del 5%
            sample_size = max(1, int(len(lines) * settings.SAMPLE_PERCENTAGE))
            sample_size = min(sample_size, 100)  # Máximo 100 líneas
            
            # Seleccionar muestra aleatoria
            selected_lines = random.sample(lines, sample_size)
            
            # Procesar según formato
            for line in selected_lines:
                line = line.strip()
                if line:
                    if file_extension == '.arff':
                        # Ignorar líneas de metadata ARFF
                        if not line.startswith('@') and not line.startswith('%'):
                            data.append(line)
                    else:
                        # Formato TXT - incluir todas las líneas de datos
                        data.append(line)
                        
    except Exception as e:
        raise Exception(f"Error procesando archivo NSL-KDD: {str(e)}")
    
    return data if data else ["No se encontraron datos procesables en el formato NSL-KDD"]

def validate_nsl_kdd_format(lines):
    """
     BACKEND: Valida formato NSL-KDD básico
    """
    if not lines:
        return False
    
    # Verificar que tenga el formato esperado (coma separada)
    sample_line = lines[0].strip() if lines else ''
    if sample_line and ',' in sample_line:
        return True
    
    return False