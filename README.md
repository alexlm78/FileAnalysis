# File Analysis

Data filling from generated files (databases dumps)

## Local installation and Execution

``` shell
uv env

source .venv/bin/activate

uv pip install -e .

# Analizar un archivo unico
analyze --file "path to file to analize" --output "path to write the output"

# Analizar un directorio
analyze --directory "path to directory to analize" --output "path to write the output"
```
