
#!/bin/bash

echo "Running Ruff..."
ruff check .

echo "Running mypy..."
mypy html_conv/ --ignore-missing-imports

echo "All checks passed!"
