# Data Cleaning Web App

A simple Streamlit web application that helps you clean your data files (CSV and Excel).

## What This App Does

This app allows you to:
1. Upload CSV or Excel files
2. View your data in a table
3. Automatically clean your data:
   - Removes duplicate rows
   - Fills empty cells with "N/A"
   - Trims extra spaces from text
   - Standardizes column names (lowercase with underscores)
4. Download the cleaned data as CSV or Excel

## How to Install and Run

### Step 1: Install Python
Make sure you have Python installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

### Step 2: Install Required Packages
Open your terminal (command prompt) and navigate to this folder, then run:

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit` - for creating the web app
- `pandas` - for working with data
- `openpyxl` - for reading/writing Excel files

### Step 3: Run the App
In the same terminal, run:

```bash
streamlit run app.py
```

This will start the app and open it in your web browser automatically!

## How to Use

1. **Upload a file**: Click "Browse files" and select your CSV or Excel file
2. **Review your data**: The app will show you a preview of your original data
3. **Automatic cleaning**: The app will automatically clean your data
4. **Download**: Click either "Download as CSV" or "Download as Excel" to save your cleaned file

## File Structure

```
cleaning/
├── app.py              # Main application code
├── requirements.txt    # List of required Python packages
└── README.md          # This file
```

## Troubleshooting

- **If the app doesn't start**: Make sure you installed all packages from `requirements.txt`
- **If you get an error uploading a file**: Make sure your file is a valid CSV or Excel file
- **If download doesn't work**: Check your browser's download settings

## Need Help?

If you encounter any issues, make sure:
- Python is installed correctly
- All packages are installed (`pip install -r requirements.txt`)
- Your file is a valid CSV or Excel format

