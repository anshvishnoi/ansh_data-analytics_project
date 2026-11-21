#!/bin/bash
# -------------------------------------------------------------
# 1-Click Launch Script for Streamlit Analytics Dashboard
# Retail Customer Sales EDA Project
# Author: Ansh Vishnoi
# -------------------------------------------------------------

set -e

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$WORKSPACE_DIR"

echo "=============================================================="
echo "🚀 Starting Retail Customer Sales Analytics Dashboard..."
echo "=============================================================="

# Check virtual environment
if [ -d ".venv" ]; then
    PYTHON_BIN=".venv/bin/python"
    STREAMLIT_BIN=".venv/bin/streamlit"
else
    PYTHON_BIN="python3"
    STREAMLIT_BIN="streamlit"
fi

# Ensure cleaned dataset and reports are generated
if [ ! -f "data/processed/cleaned_retail_sales_dataset.csv" ]; then
    echo "⚙️ First run: Generating cleaned dataset and analytical reports..."
    $PYTHON_BIN -m src.generate_eda_reports
fi

echo "🌐 Launching Streamlit web server on http://localhost:8501..."
$STREAMLIT_BIN run app/main.py --server.headless=false --server.port=8501
