import os
import argparse
from analysis.analysis import analyze_file, analyze_directory
from analysis.utils import export_results

def main():
   parser = argparse.ArgumentParser(description='Analizar el porcentaje de llenado de columnas en archivos Excel o CSV.')
   parser.add_argument('--file', type=str, help='Ruta al archivo a analizar')
   parser.add_argument('--directory', type=str, help='Ruta al directorio que contiene los archivos a analizar')
   parser.add_argument('--output', type=str, default='results', help='Directorio donde se guardarán los resultados')
   
   args = parser.parse_args()
   
   # Definir valores válidos para columnas específicas (personaliza según tus necesidades)
   # Ejemplo: para la columna 'ESTADO', 'S' y 'N' se consideran valores válidos
   valid_values = {
      'COMPRABLE': {'S', ' ', ''},
      'VENDIBLE': {'S', ' ', ''},
      # Agrega más columnas según sea necesario
   }
   
   if args.archivo:
      # Analizar un solo archivo
      result = analyze_file(args.archivo, valid_values)
      print("\nResultados:")
      print(result)
      
      # Exportar resultados
      if not os.path.exists(args.salida):
         os.makedirs(args.salida)
      base_name = os.path.splitext(os.path.basename(args.archivo))[0]
      output_path = os.path.join(args.salida, f"{base_name}_analisis.xlsx")
      result.to_excel(output_path, index=False)
      print(f"\nResultados guardados en: {output_path}")
      
   elif args.directorio:
      # Analizar todos los archivos en un directorio
      results = analyze_directory(args.directorio, valid_values)
      export_results(results, args.salida)
   else:
      print("Debes especificar --archivo o --directorio para indicar qué analizar.")

if __name__ == "__main__":
   main()
   