import pytest
import pandas as pd
from unittest.mock import patch
from analysis.cli import main

class TestCLI:
    """Tests for the command line interface."""
    
    @patch('sys.argv', ['analyze', '--file', 'dummy_path.csv', '--output', 'dummy_output'])
    @patch('analysis.cli.analyze_file')
    @patch('pd.DataFrame.to_excel')
    def test_cli_single_file(self, mock_to_excel, mock_analyze_file, sample_csv_path):
        """Test CLI with a single file argument."""
        # Mock the analyze_file function to return a sample DataFrame
        mock_df = pd.DataFrame({
            'Column': ['A', 'B'],
            'Total_Rows': [3, 3],
            'Full_Values': [3, 2],
            'Empty_Values': [0, 1],
            'Percentage_Filled': [100.0, 66.67]
        })
        mock_analyze_file.return_value = mock_df
        
        # Call the main function
        with patch('sys.argv', ['analyze', '--file', sample_csv_path, '--output', 'dummy_output']):
            main()
        
        # Check that analyze_file was called with the correct arguments
        mock_analyze_file.assert_called_once()
        args, kwargs = mock_analyze_file.call_args
        assert args[0] == sample_csv_path
        assert 'valid_values' in kwargs
        
        # Check that to_excel was called
        assert mock_to_excel.called
    
    @patch('analysis.cli.analyze_directory')
    @patch('analysis.cli.export_results')
    def test_cli_directory(self, mock_export_results, mock_analyze_directory, sample_directory):
        """Test CLI with a directory argument."""
        # Mock the analyze_directory function to return a sample dictionary
        mock_results = {
            'file1.csv': pd.DataFrame({
                'Column': ['A', 'B'],
                'Total_Rows': [3, 3],
                'Full_Values': [3, 2],
                'Empty_Values': [0, 1],
                'Percentage_Filled': [100.0, 66.67]
            })
        }
        mock_analyze_directory.return_value = mock_results
        
        # Call the main function
        with patch('sys.argv', ['analyze', '--directory', sample_directory, '--output', 'dummy_output']):
            main()
        
        # Check that analyze_directory was called with the correct arguments
        mock_analyze_directory.assert_called_once()
        args, kwargs = mock_analyze_directory.call_args
        assert args[0] == sample_directory
        assert 'valid_values' in kwargs
        
        # Check that export_results was called with the correct arguments
        mock_export_results.assert_called_once_with(mock_results, 'dummy_output')
    
    @patch('builtins.print')
    def test_cli_no_arguments(self, mock_print):
        """Test CLI with no file or directory arguments."""
        # Call the main function with no arguments
        with patch('sys.argv', ['analyze']):
            with pytest.raises(SystemExit):
                main()
        
        # Check that an error message was printed
        assert mock_print.called
        assert any("You must specify --file or --directory" in str(args) for args, _ in mock_print.call_args_list)
