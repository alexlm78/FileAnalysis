import os
import argparse
from analysis.analysis import analyze_file, analyze_directory
from analysis.utils import export_results

def main():
   parser = argparse.ArgumentParser(
      description='Analyze the percentage of columns filled in Excel or CSV files.',
      add_help=True
   )
   parser.add_argument('--file', type=str, help='Path to the file to be analyzed.')
   parser.add_argument('--directory', type=str, help='Path to the directory containing the files to be analyzed.')
   parser.add_argument('--output', type=str, default='results', help='Directory where the results will be stored')
   
   args = parser.parse_args()
   
   # Define valid values for specific columns (customize according to your needs)
   # Example: for the column 'COMPRABLE', 'Y', ' ' and '' are considered as valid values
   valid_values = {
      'COMPRABLE': {'S', ' ', ''},
      'VENDIBLE': {'S', ' ', ''},
      # Add more columns as needed
   }
   
   if args.file:
      # Analyze a single file
      result = analyze_file(args.file, valid_values)
      print("\nResultados:")
      print(result)
      
      # Export results
      if not os.path.exists(args.output):
         os.makedirs(args.output)
      base_name = os.path.splitext(os.path.basename(args.file))[0]
      output_path = os.path.join(args.output, f"{base_name}_analysis.xlsx")
      result.to_excel(output_path, index=False)
      print(f"\nResults will be saved at: {output_path}")
      
   elif args.directory:
      # Scan all files in a directory
      results = analyze_directory(args.directory, valid_values)
      export_results(results, args.output)
   else:
      print("You must specify --file or --directory to indicate what to scan.")
      parser.print_help()

if __name__ == "__main__":
   main()
   