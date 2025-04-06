import os
import pandas as pd
from typing import Dict

def export_results(results: Dict[str, pd.DataFrame], output_dir: str) -> None:
   """
   Exporta los resultados a archivos Excel.
   
   Args:
      results: Diccionario con nombres de archivos como claves y DataFrames de resultados como valores
      output_dir: Directorio donde se guardarán los resultados
   """
   # Crear directorio de salida si no existe
   if not os.path.exists(output_dir):
      os.makedirs(output_dir)
   
   # Crear un archivo Excel para cada resultado
   for filename, result_df in results.items():
      base_name = os.path.splitext(filename)[0]
      output_path = os.path.join(output_dir, f"{base_name}_analisis.xlsx")
      result_df.to_excel(output_path, index=False)
      print(f"Resultados guardados en: {output_path}")
   
   # Crear un archivo Excel con todos los resultados combinados
   all_results = pd.DataFrame()
   for filename, result_df in results.items():
      result_df['Archivo'] = filename
      all_results = pd.concat([all_results, result_df])
   
   all_results_path = os.path.join(output_dir, "complete_analysis.xlsx")
   all_results.to_excel(all_results_path, index=False)
   print(f"Conbined Results saved in: {all_results_path}")
