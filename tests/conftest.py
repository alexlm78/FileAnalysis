import os
import pandas as pd
import pytest
import tempfile
import shutil

@pytest.fixture
def sample_csv_path():
    """Create a sample CSV file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        # Create a sample DataFrame
        df = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'NAME': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
            'PRICE': [10.5, 20.0, None, 15.75, 8.25],
            'IN_STOCK': ['Y', 'N', 'Y', '', None],
            'COMPRABLE': ['S', 'S', '', ' ', 'S'],
            'VENDIBLE': ['S', '', 'S', ' ', 'S'],
        })
        
        # Save the DataFrame to a CSV file
        df.to_csv(tmp.name, index=False)
        yield tmp.name
    
    # Clean up after the test
    if os.path.exists(tmp.name):
        os.remove(tmp.name)

@pytest.fixture
def sample_excel_path():
    """Create a sample Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        # Create a sample DataFrame
        df = pd.DataFrame({
            'ID': [1, 2, 3, 4, 5],
            'NAME': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
            'PRICE': [10.5, 20.0, None, 15.75, 8.25],
            'IN_STOCK': ['Y', 'N', 'Y', '', None],
            'COMPRABLE': ['S', 'S', '', ' ', 'S'],
            'VENDIBLE': ['S', '', 'S', ' ', 'S'],
        })
        
        # Save the DataFrame to an Excel file
        df.to_excel(tmp.name, index=False)
        yield tmp.name
    
    # Clean up after the test
    if os.path.exists(tmp.name):
        os.remove(tmp.name)

@pytest.fixture
def sample_directory():
    """Create a temporary directory with sample files for testing."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Create sample CSV file in the directory
    csv_path = os.path.join(temp_dir, "sample1.csv")
    df1 = pd.DataFrame({
        'ID': [1, 2, 3],
        'NAME': ['Item A', 'Item B', 'Item C'],
        'STATUS': ['Active', None, 'Inactive']
    })
    df1.to_csv(csv_path, index=False)
    
    # Create sample Excel file in the directory
    excel_path = os.path.join(temp_dir, "sample2.xlsx")
    df2 = pd.DataFrame({
        'CODE': ['A001', 'A002', 'A003'],
        'DESCRIPTION': ['Description 1', 'Description 2', ''],
        'COMPRABLE': ['S', '', 'S']
    })
    df2.to_excel(excel_path, index=False)
    
    # Create a non-supported file in the directory (to test filtering)
    txt_path = os.path.join(temp_dir, "sample3.txt")
    with open(txt_path, 'w') as f:
        f.write("This is a text file that should be ignored.")
    
    yield temp_dir
    
    # Clean up after the test
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

@pytest.fixture
def output_directory():
    """Create a temporary directory for test outputs."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
    # Clean up after the test
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
