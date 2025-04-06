import os
import pandas as pd
from typing import Dict

def export_results(results: Dict[str, pd.DataFrame], output_dir: str) -> None:
   """
   Exports the results to Excel files.
   
   Args:
      results: Dictionary with file names as keys and result DataFrames as values
      output_dir: Directory where the results will be saved.
   """
   # Create output directory if it does not exist
   if not os.path.exists(output_dir):
      os.makedirs(output_dir)
   
   # Create an Excel file for each result
   for filename, result_df in results.items():
      base_name = os.path.splitext(filename)[0]
      output_path = os.path.join(output_dir, f"{base_name}_analisis.xlsx")
      result_df.to_excel(output_path, index=False)
      print(f"Resultados guardados en: {output_path}")
   
   # Create an Excel file with all results combined
   all_results = pd.DataFrame()
   for filename, result_df in results.items():
      result_df['File'] = filename
      all_results = pd.concat([all_results, result_df])
   
   all_results_path = os.path.join(output_dir, "complete_analysis.xlsx")
   all_results.to_excel(all_results_path, index=False)
   print(f"Conbined Results saved in: {all_results_path}")
