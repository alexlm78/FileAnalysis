import os
import pandas
from typing import Dict, Set

def analyze_file(file_path: str, valid_values: Dict[str, Set] = None) -> pandas.DataFrame:
   """
   Parses an Excel or CSV file and calculates the fill percentage of each column.
   
   Args:
      file_path: Path to the file to analyze
      valid_values: Dictionary with column names as keys and valid value sets as values
         For example: {'STATUS': {'Y', 'N'}}}
   
   Returns:
      DataFrame with fill statistics for each column
   """
   #  Determine the file type
   file_extension = os.path.splitext(file_path)[1].lower()
   
   # Load the file according to its extension
   if file_extension == '.csv':
      df = pandas.read_csv(file_path, low_memory=False)
   elif file_extension in ['.xlsx', '.xls']:
      df = pandas.read_excel(file_path)
   else:
      raise ValueError(f"File type not supported: {file_extension}")
   
   # Initialize the dictionary to store results
   results = {
      'Column': [],
      'Total_Rows': [],
      'Full_Values': [],
      'Empty_Values': [],
      'Percentage_Filled': []
   }
   
   # If a dictionary of valid values was not provided, create an empty one
   if valid_values is None:
      valid_values = {}
   
   total_rows = len(df)
   
   # Analyze every column
   for column in df.columns:
      # If the columns had valid specific values
      if column in valid_values:
         # Count values that are in the set of valid values. 
         valid_count = df[column].isin(valid_values[column]).sum()
         empty_count = total_rows - valid_count
      else:
         # Count non-null and non-empty values
         valid_count = df[column].notna().sum()
         # For strings, check also if empty
         if df[column].dtype == 'object':
               valid_count = (df[column].notna() & (df[column] != '')).sum()
         empty_count = total_rows - valid_count
      
      # Calculate filling percentage
      fill_percentage = (valid_count / total_rows * 100) if total_rows > 0 else 0
      
      # Save results
      results['Column'].append(column)
      results['Total_Rows'].append(total_rows)
      results['Full_Values'].append(valid_count)
      results['Empty_Values'].append(empty_count)
      results['Percentage_Filled'].append(round(fill_percentage, 2))
   
   # Create DataFrame with the results
   results_df = pandas.DataFrame(results)
   return results_df

def analyze_directory(directory_path: str, valid_values: Dict[str, Set] = None) -> Dict[str, pandas.DataFrame]:
   """
   Analyzes all Excel and CSV files in a directory.
   
   Args:
      directory_path: Path to the directory containing the files
      valid_values: Dictionary with valid values per column
   
   Returns:
      Dictionary with file names as keys and result DataFrames as values.
   """
   results = {}
   
   for filename in os.listdir(directory_path):
      file_path = os.path.join(directory_path, filename)
      if os.path.isfile(file_path) and filename.lower().endswith(('.csv', '.xlsx', '.xls')):
         try:
               file_results = analyze_file(file_path, valid_values)
               results[filename] = file_results
               print(f"Analysis completed for: {filename}")
         except Exception as e:
               print(f"Error analyzing {filename}: {str(e)}")
   
   return results