import os
import pytest
import pandas as pd
from analysis.utils import export_results

class TestExportResults:
    """Tests for the export_results function."""
    
    def test_export_results(self, sample_csv_path, output_directory):
        """Test exporting analysis results to Excel files."""
        # Create some sample analysis results
        result1 = pd.DataFrame({
            'Column': ['ID', 'NAME', 'PRICE'],
            'Total_Rows': [5, 5, 5],
            'Full_Values': [5, 5, 3],
            'Empty_Values': [0, 0, 2],
            'Percentage_Filled': [100.0, 100.0, 60.0]
        })
        
        result2 = pd.DataFrame({
            'Column': ['CODE', 'DESCRIPTION'],
            'Total_Rows': [3, 3],
            'Full_Values': [3, 2],
            'Empty_Values': [0, 1],
            'Percentage_Filled': [100.0, 66.67]
        })
        
        # Create a dictionary of results
        results = {
            'file1.csv': result1,
            'file2.xlsx': result2
        }
        
        # Export the results
        export_results(results, output_directory)
        
        # Check that the expected output files were created
        expected_files = [
            os.path.join(output_directory, "file1_analisis.xlsx"),
            os.path.join(output_directory, "file2_analisis.xlsx"),
            os.path.join(output_directory, "complete_analysis.xlsx")
        ]
        
        for file_path in expected_files:
            assert os.path.exists(file_path), f"Expected output file {file_path} does not exist"
        
        # Check the content of the individual result files
        df1 = pd.read_excel(os.path.join(output_directory, "file1_analisis.xlsx"))
        assert len(df1) == len(result1)
        assert all(col in df1.columns for col in result1.columns)
        
        df2 = pd.read_excel(os.path.join(output_directory, "file2_analisis.xlsx"))
        assert len(df2) == len(result2)
        assert all(col in df2.columns for col in result2.columns)
        
        # Check the content of the combined results file
        all_results = pd.read_excel(os.path.join(output_directory, "complete_analysis.xlsx"))
        assert len(all_results) == len(result1) + len(result2)
        assert 'File' in all_results.columns
        
        # Check that the file names are correctly included
        file1_rows = all_results[all_results['File'] == 'file1.csv']
        file2_rows = all_results[all_results['File'] == 'file2.xlsx']
        assert len(file1_rows) == len(result1)
        assert len(file2_rows) == len(result2)
    
    def test_export_results_empty(self, output_directory):
        """Test exporting empty results."""
        # Export empty results
        export_results({}, output_directory)
        
        # Check that the combined results file exists (even if empty)
        combined_file = os.path.join(output_directory, "complete_analysis.xlsx")
        assert os.path.exists(combined_file)
        
        # Verify that the file contains an empty DataFrame
        all_results = pd.read_excel(combined_file)
        assert len(all_results) == 0
    
    def test_export_results_directory_creation(self, tmp_path):
        """Test that the output directory is created if it doesn't exist."""
        # Create a path to a non-existent directory
        output_dir = os.path.join(tmp_path, "new_dir", "results")
        
        # Create some sample results
        results = {
            'test.csv': pd.DataFrame({
                'Column': ['A', 'B'],
                'Total_Rows': [2, 2],
                'Full_Values': [2, 1],
                'Empty_Values': [0, 1],
                'Percentage_Filled': [100.0, 50.0]
            })
        }
        
        # Export the results to the non-existent directory
        export_results(results, output_dir)
        
        # Check that the directory was created
        assert os.path.exists(output_dir)
        
        # Check that the expected files were created
        expected_files = [
            os.path.join(output_dir, "test_analisis.xlsx"),
            os.path.join(output_dir, "complete_analysis.xlsx")
        ]
        
        for file_path in expected_files:
            assert os.path.exists(file_path)
