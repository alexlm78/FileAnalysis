import os
import pandas as pd
from typing import Dict, List, Set, Union, Optional

def analyze_file(file_path: str, valid_values: Dict[str, Set] = None) -> pd.DataFrame:
   """
   Analiza un archivo Excel o CSV y calcula el porcentaje de llenado de cada columna.
   
   Args:
      file_path: Ruta al archivo a analizar
      valid_values: Diccionario con nombres de columnas como claves y conjuntos de valores válidos como valores
                  Por ejemplo: {'ESTADO': {'S', 'N'}}
   
   Returns:
      DataFrame con estadísticas de llenado para cada columna
   """
   # Determinar el tipo de archivo
   file_extension = os.path.splitext(file_path)[1].lower()
   
   # Cargar el archivo según su extensión
   if file_extension == '.csv':
      df = pd.read_csv(file_path, low_memory=False)
   elif file_extension in ['.xlsx', '.xls']:
      df = pd.read_excel(file_path)
   else:
      raise ValueError(f"Tipo de archivo no soportado: {file_extension}")
   
   # Inicializar el diccionario para almacenar resultados
   results = {
      'Columna': [],
      'Total_Filas': [],
      'Valores_Llenos': [],
      'Valores_Vacios': [],
      'Porcentaje_Llenado': []
   }
   
   # Si no se proporcionó un diccionario de valores válidos, crear uno vacío
   if valid_values is None:
      valid_values = {}
   
   total_rows = len(df)
   
   # Analizar cada columna
   for column in df.columns:
      # Si la columna tiene valores válidos específicos definidos
      if column in valid_values:
         # Contar valores que están en el conjunto de valores válidos
         valid_count = df[column].isin(valid_values[column]).sum()
         empty_count = total_rows - valid_count
      else:
         # Contar valores no nulos y no vacíos
         valid_count = df[column].notna().sum()
         # Para strings, verificar también si está vacío
         if df[column].dtype == 'object':
               valid_count = (df[column].notna() & (df[column] != '')).sum()
         empty_count = total_rows - valid_count
      
      # Calcular porcentaje de llenado
      fill_percentage = (valid_count / total_rows * 100) if total_rows > 0 else 0
      
      # Guardar resultados
      results['Columna'].append(column)
      results['Total_Filas'].append(total_rows)
      results['Valores_Llenos'].append(valid_count)
      results['Valores_Vacios'].append(empty_count)
      results['Porcentaje_Llenado'].append(round(fill_percentage, 2))
   
   # Crear DataFrame con los resultados
   results_df = pd.DataFrame(results)
   return results_df

def analyze_directory(directory_path: str, valid_values: Dict[str, Set] = None) -> Dict[str, pd.DataFrame]:
   """
   Analiza todos los archivos Excel y CSV en un directorio.
   
   Args:
      directory_path: Ruta al directorio que contiene los archivos
      valid_values: Diccionario con valores válidos por columna
   
   Returns:
      Diccionario con nombres de archivos como claves y DataFrames de resultados como valores
   """
   results = {}
   
   for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if os.path.isfile(file_path) and filename.lower().endswith(('.csv', '.xlsx', '.xls')):
         try:
               file_results = analyze_file(file_path, valid_values)
               results[filename] = file_results
               print(f"Análisis completado para: {filename}")
         except Exception as e:
               print(f"Error al analizar {filename}: {str(e)}")
   
   return results