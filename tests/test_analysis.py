import os
import pytest
import pandas as pd
from analysis.analysis import analyze_file, analyze_directory

class TestAnalyzeFile:
    """Tests for the analyze_file function."""
    
    def test_analyze_csv(self, sample_csv_path):
        """Test analyzing a CSV file."""
        result = analyze_file(sample_csv_path)
        
        # Check that the result is a DataFrame
        assert isinstance(result, pd.DataFrame)
        
        # Check that the result has the expected columns
        expected_columns = ['Column', 'Total_Rows', 'Full_Values', 'Empty_Values', 'Percentage_Filled']
        assert all(col in result.columns for col in expected_columns)
        
        # Check that all columns from the input file are analyzed
        input_columns = pd.read_csv(sample_csv_path).columns
        analyzed_columns = result['Column'].tolist()
        assert all(col in analyzed_columns for col in input_columns)
        
        # Check that the total rows count is correct
        expected_rows = len(pd.read_csv(sample_csv_path))
        assert all(result['Total_Rows'] == expected_rows)
    
    def test_analyze_excel(self, sample_excel_path):
        """Test analyzing an Excel file."""
        result = analyze_file(sample_excel_path)
        
        # Check that the result is a DataFrame
        assert isinstance(result, pd.DataFrame)
        
        # Check that the result has the expected columns
        expected_columns = ['Column', 'Total_Rows', 'Full_Values', 'Empty_Values', 'Percentage_Filled']
        assert all(col in result.columns for col in expected_columns)
        
        # Check that all columns from the input file are analyzed
        input_columns = pd.read_excel(sample_excel_path).columns
        analyzed_columns = result['Column'].tolist()
        assert all(col in analyzed_columns for col in input_columns)
        
        # Check that the total rows count is correct
        expected_rows = len(pd.read_excel(sample_excel_path))
        assert all(result['Total_Rows'] == expected_rows)
    
    def test_analyze_with_valid_values(self, sample_csv_path):
        """Test analyzing a file with specified valid values."""
        # Define some valid values for specific columns
        valid_values = {
            'COMPRABLE': {'S', ' ', ''},
            'VENDIBLE': {'S', ' ', ''}
        }
        
        result = analyze_file(sample_csv_path, valid_values)
        
        # Check that the result is a DataFrame
        assert isinstance(result, pd.DataFrame)
        
        # Find the rows for COMPRABLE and VENDIBLE columns
        comprable_row = result[result['Column'] == 'COMPRABLE']
        vendible_row = result[result['Column'] == 'VENDIBLE']
        
        # Verify that values are counted correctly according to valid_values
        assert comprable_row['Full_Values'].iloc[0] == 5  # All values are valid
        
        # Manually calculate expected counts for validation
        df = pd.read_csv(sample_csv_path)
        expected_vendible_valid = sum(df['VENDIBLE'].isin(['S', ' ', '']))
        assert vendible_row['Full_Values'].iloc[0] == expected_vendible_valid
    
    def test_unsupported_file_type(self):
        """Test that an unsupported file type raises a ValueError."""
        with tempfile.NamedTemporaryFile(suffix='.txt') as tmp:
            with pytest.raises(ValueError) as excinfo:
                analyze_file(tmp.name)
            
            assert "File type not supported" in str(excinfo.value)

class TestAnalyzeDirectory:
    """Tests for the analyze_directory function."""
    
    def test_analyze_directory(self, sample_directory):
        """Test analyzing a directory with multiple files."""
        results = analyze_directory(sample_directory)
        
        # Check that we got results for each supported file
        expected_files = ["sample1.csv", "sample2.xlsx"]
        assert all(filename in results for filename in expected_files)
        assert "sample3.txt" not in results  # Text file should be ignored
        
        # Check that each result is a DataFrame with the expected structure
        for filename, result in results.items():
            assert isinstance(result, pd.DataFrame)
            expected_columns = ['Column', 'Total_Rows', 'Full_Values', 'Empty_Values', 'Percentage_Filled']
            assert all(col in result.columns for col in expected_columns)
    
    def test_analyze_directory_with_valid_values(self, sample_directory):
        """Test analyzing a directory with specified valid values."""
        valid_values = {
            'COMPRABLE': {'S', ' ', ''}
        }
        
        results = analyze_directory(sample_directory, valid_values)
        
        # Check sample2.xlsx which has COMPRABLE column
        sample2_result = results["sample2.xlsx"]
        comprable_row = sample2_result[sample2_result['Column'] == 'COMPRABLE']
        
        # Verify that values are counted correctly according to valid_values
        # All COMPRABLE values in sample2.xlsx fixture should be valid
        assert comprable_row['Full_Values'].iloc[0] == 3
    
    def test_empty_directory(self):
        """Test analyzing an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            results = analyze_directory(temp_dir)
            assert results == {}
