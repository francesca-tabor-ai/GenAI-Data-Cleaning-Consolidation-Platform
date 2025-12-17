"""
Data Cleaning Web App using Streamlit
=====================================
This app allows you to upload CSV or Excel files, clean them, and download the cleaned data.

What this app does:
1. Upload CSV or Excel files
2. Display the data in a table
3. Clean the data (remove duplicates, handle missing values, trim spaces, standardize column names)
4. Download the cleaned file as CSV or Excel
5. For Excel files with multiple sheets, all sheets are preserved and cleaned separately
"""

# Import the necessary libraries
# Streamlit is used to create the web interface
import streamlit as st

# Pandas is used to work with data (like Excel spreadsheets)
import pandas as pd

# io is used to handle file operations in memory
from io import BytesIO

# Set the page title and layout
st.set_page_config(
    page_title="Data Cleaning App",
    page_icon="🧹",
    layout="wide"
)

# Display a title at the top of the page
st.title("🧹 Data Cleaning App")
st.markdown("Upload your CSV or Excel file, clean it, and download the result!")
st.markdown("💡 **Note:** For Excel files with multiple sheets, all sheets will be preserved and cleaned separately!")

# ============================================================================
# HELPER FUNCTION: CLEAN A SINGLE DATAFRAME
# ============================================================================
def clean_dataframe(df):
    """
    This function takes a DataFrame and cleans it.
    It returns the cleaned DataFrame and a summary of what was cleaned.
    
    Parameters:
    - df: The original DataFrame to clean
    
    Returns:
    - df_cleaned: The cleaned DataFrame
    - summary: A dictionary with cleaning statistics
    """
    # Create a copy of the data to clean (so we don't modify the original)
    df_cleaned = df.copy()
    
    # --- Cleaning Step 1: Remove Duplicate Rows ---
    # Duplicates are rows that are exactly the same
    rows_before = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates()  # Remove duplicate rows
    rows_after = len(df_cleaned)
    duplicates_removed = rows_before - rows_after
    
    # --- Cleaning Step 2: Handle Missing Values ---
    # Missing values are empty cells in the data
    # Fill all empty cells with "N/A"
    df_cleaned = df_cleaned.fillna("N/A")
    
    # --- Cleaning Step 3: Trim Extra Spaces from Text ---
    # Sometimes text has extra spaces at the beginning or end
    # This removes those extra spaces from all text columns
    
    # Go through each column
    for col in df_cleaned.columns:
        # Check if the column contains text (string) data
        if df_cleaned[col].dtype == 'object':  # 'object' usually means text
            # Remove extra spaces from the beginning and end of each value
            df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
    
    # --- Cleaning Step 4: Standardize Column Names ---
    # Make column names lowercase and replace spaces with underscores
    # Example: "First Name" becomes "first_name"
    
    # Create a dictionary to rename columns
    # This will map old column names to new standardized names
    new_column_names = {}
    
    for old_name in df_cleaned.columns:
        # Convert to lowercase and replace spaces with underscores
        new_name = old_name.lower().replace(' ', '_')
        new_column_names[old_name] = new_name
    
    # Apply the new column names
    df_cleaned = df_cleaned.rename(columns=new_column_names)
    
    # Create a summary dictionary
    summary = {
        'duplicates_removed': duplicates_removed,
        'rows_before': rows_before,
        'rows_after': rows_after,
        'columns': len(df_cleaned.columns)
    }
    
    return df_cleaned, summary

# ============================================================================
# STEP 1: FILE UPLOAD
# ============================================================================
# This section creates a file uploader widget
# Users can click to select a file from their computer
st.header("Step 1: Upload Your File")

# Create a file uploader that accepts CSV and Excel files
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=['csv', 'xlsx', 'xls'],  # Only allow these file types
    help="Select a CSV or Excel file from your computer"
)

# ============================================================================
# STEP 2: DISPLAY AND CLEAN DATA
# ============================================================================
# Only proceed if a file has been uploaded
if uploaded_file is not None:
    try:
        # Check the file type and read it accordingly
        is_excel = uploaded_file.name.endswith(('.xlsx', 'xls'))
        is_csv = uploaded_file.name.endswith('.csv')
        
        if is_csv:
            # ====================================================================
            # CSV FILE HANDLING (Single sheet)
            # ====================================================================
            # If it's a CSV file, use pd.read_csv()
            # CSV files only have one sheet, so we read it directly
            df = pd.read_csv(uploaded_file)
            
            # Store in a dictionary format for consistent processing
            # Use 'Sheet1' as the default name for CSV files
            data_sheets = {'Sheet1': df}
            sheet_names = ['Sheet1']
            
        else:
            # ====================================================================
            # EXCEL FILE HANDLING (Multiple sheets)
            # ====================================================================
            # If it's an Excel file, read ALL sheets
            # sheet_name=None tells pandas to read all sheets
            # This returns a dictionary where keys are sheet names and values are DataFrames
            data_sheets = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl')
            sheet_names = list(data_sheets.keys())
            
            # Display information about sheets found
            st.info(f"📋 Found {len(sheet_names)} sheet(s) in your Excel file: {', '.join(sheet_names)}")
        
        # Display information about the original data
        st.header("Step 2: Original Data")
        
        # Show summary for all sheets
        total_rows = sum(len(df) for df in data_sheets.values())
        total_cols = sum(len(df.columns) for df in data_sheets.values())
        st.info(f"📊 Total: {total_rows} rows and {total_cols} columns across {len(sheet_names)} sheet(s)")
        
        # Display original data for each sheet
        # Use tabs if there are multiple sheets, otherwise just show the data
        if len(sheet_names) > 1:
            # Create tabs for each sheet
            tabs = st.tabs(sheet_names)
            for i, (tab, sheet_name) in enumerate(zip(tabs, sheet_names)):
                with tab:
                    st.subheader(f"Sheet: {sheet_name}")
                    st.dataframe(data_sheets[sheet_name], use_container_width=True)
                    st.caption(f"Rows: {len(data_sheets[sheet_name])}, Columns: {len(data_sheets[sheet_name].columns)}")
        else:
            # Single sheet - just display it
            st.subheader(f"Preview of Original Data ({sheet_names[0]})")
            st.dataframe(data_sheets[sheet_names[0]], use_container_width=True)
        
        # ========================================================================
        # STEP 3: DATA CLEANING
        # ========================================================================
        st.header("Step 3: Clean Your Data")
        
        # Clean each sheet separately
        cleaned_sheets = {}
        cleaning_summaries = {}
        
        # Show progress for multiple sheets
        if len(sheet_names) > 1:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Clean each sheet one by one
        for idx, sheet_name in enumerate(sheet_names):
            if len(sheet_names) > 1:
                # Update progress
                progress = (idx + 1) / len(sheet_names)
                progress_bar.progress(progress)
                status_text.text(f"Cleaning sheet {idx + 1} of {len(sheet_names)}: {sheet_name}")
            
            # Clean this sheet using our helper function
            df_cleaned, summary = clean_dataframe(data_sheets[sheet_name])
            cleaned_sheets[sheet_name] = df_cleaned
            cleaning_summaries[sheet_name] = summary
        
        # Clear progress indicators
        if len(sheet_names) > 1:
            progress_bar.empty()
            status_text.empty()
        
        # Display cleaning summary
        st.success(f"✅ Data cleaning completed for {len(sheet_names)} sheet(s)!")
        
        # Show summary for each sheet
        if len(sheet_names) > 1:
            # Multiple sheets - show summary in expandable sections
            for sheet_name in sheet_names:
                summary = cleaning_summaries[sheet_name]
                with st.expander(f"📊 Cleaning Summary: {sheet_name}", expanded=False):
                    st.write(f"""
                    - **Rows before:** {summary['rows_before']}
                    - **Rows after:** {summary['rows_after']}
                    - **Duplicates removed:** {summary['duplicates_removed']}
                    - **Columns:** {summary['columns']}
                    - **Missing values filled with:** N/A
                    - **Extra spaces trimmed:** Yes
                    - **Column names standardized:** Yes
                    """)
        else:
            # Single sheet - show simple summary
            summary = cleaning_summaries[sheet_names[0]]
            st.info(f"""
            **Cleaning Summary:**
            - Duplicate rows removed: {summary['duplicates_removed']}
            - Missing values filled with: N/A
            - Extra spaces trimmed from text
            - Column names standardized (lowercase with underscores)
            """)
        
        # Show the cleaned data
        st.subheader("Preview of Cleaned Data")
        
        # Display cleaned data for each sheet
        if len(sheet_names) > 1:
            # Create tabs for cleaned data
            cleaned_tabs = st.tabs([f"Cleaned: {name}" for name in sheet_names])
            for i, (tab, sheet_name) in enumerate(zip(cleaned_tabs, sheet_names)):
                with tab:
                    st.dataframe(cleaned_sheets[sheet_name], use_container_width=True)
                    st.caption(f"Rows: {len(cleaned_sheets[sheet_name])}, Columns: {len(cleaned_sheets[sheet_name].columns)}")
        else:
            # Single sheet - just display it
            st.dataframe(cleaned_sheets[sheet_names[0]], use_container_width=True)
        
        # ========================================================================
        # STEP 4: DOWNLOAD CLEANED DATA
        # ========================================================================
        st.header("Step 4: Download Your Cleaned File")
        
        # Create two columns for the download buttons (side by side)
        col1, col2 = st.columns(2)
        
        with col1:
            # --- Download as CSV ---
            # For CSV download, we only download the first sheet
            # (CSV files can only have one sheet)
            if len(sheet_names) > 1:
                st.warning("⚠️ CSV files can only contain one sheet. Downloading the first sheet only.")
            
            # Convert the first cleaned sheet to CSV format
            first_sheet_name = sheet_names[0]
            csv_data = cleaned_sheets[first_sheet_name].to_csv(index=False).encode('utf-8')
            
            # Create a download button for CSV
            st.download_button(
                label="📥 Download as CSV",
                data=csv_data,
                file_name="cleaned_data.csv",  # Name of the downloaded file
                mime="text/csv",  # File type
                help="Click to download the cleaned data as a CSV file (first sheet only)"
            )
        
        with col2:
            # --- Download as Excel ---
            # Create an Excel file in memory using BytesIO
            # BytesIO creates a file-like object in memory (not on disk)
            excel_buffer = BytesIO()
            
            # Write ALL cleaned sheets to the Excel file
            # Use ExcelWriter to write multiple sheets
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                # Write each cleaned sheet to the Excel file
                for sheet_name in sheet_names:
                    # Write the cleaned DataFrame to a sheet with the same name
                    cleaned_sheets[sheet_name].to_excel(
                        writer, 
                        sheet_name=sheet_name,  # Keep the original sheet name
                        index=False  # Don't include row numbers
                    )
            
            excel_buffer.seek(0)  # Go back to the beginning of the file
            
            # Create a download button for Excel
            st.download_button(
                label="📥 Download as Excel",
                data=excel_buffer,
                file_name="cleaned_data.xlsx",  # Name of the downloaded file
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # Excel file type
                help="Click to download the cleaned data as an Excel file (all sheets preserved)"
            )
            
            if len(sheet_names) > 1:
                st.caption(f"✅ All {len(sheet_names)} sheet(s) will be included in the Excel file")
    
    except Exception as e:
        # If something goes wrong, show an error message
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please make sure you uploaded a valid CSV or Excel file.")

else:
    # Show instructions when no file is uploaded
    st.info("👆 Please upload a CSV or Excel file to get started!")

# ============================================================================
# FOOTER
# ============================================================================
# Add some helpful information at the bottom
st.markdown("---")
st.markdown("""
### 💡 How to Use This App:
1. **Upload**: Click "Browse files" and select your CSV or Excel file
2. **Review**: Check the preview of your original data (all sheets if Excel)
3. **Clean**: The app automatically cleans your data (each sheet separately)
4. **Download**: Click the download button to save your cleaned file

### 🧹 What Gets Cleaned:
- ✅ Duplicate rows are removed from each sheet
- ✅ Empty cells are filled with "N/A"
- ✅ Extra spaces are trimmed from text
- ✅ Column names are standardized (lowercase with underscores)

### 📋 Multiple Sheets Support:
- ✅ Excel files with multiple sheets are fully supported
- ✅ Each sheet is cleaned separately
- ✅ All sheets are preserved in the downloaded Excel file
- ✅ CSV download only includes the first sheet (CSV format limitation)
""")

