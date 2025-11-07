# FindingExcellence

A powerful tool for finding and searching content within Excel files in your Desktop and Downloads folders.

![FindingExcellence_new_logo](resources/FindingExcellence_new_logo.png)

## Features

- Search for Excel files by filename in both Desktop and Downloads folders simultaneously
- Search within Excel file contents for specific keywords
- Case-sensitive and case-insensitive search options
- Date range filtering for file modification times
- Interactive and detailed search results
- Export results to CSV or text files
- Support for .xls, .xlsx, and .xlsm files
- Keyboard shortcuts for improved productivity

## Screenshots

*Note: Add screenshots of your application here for better user understanding*

## Installation Options

### Option 1: Using Virtual Environment (Recommended)

1. **Quick Setup with Interactive Menu:**
   ```
   dev_menu.bat
   ```
   Select option 1 to create isolated environment with exact versions

2. **Manual Setup:**
   ```
   setup_venv.bat
   ```

3. **Run the application:**
   ```
   activate_venv.bat
   python main.py
   ```

### Option 2: Build Executable (End Users)

1. **Create executable with isolated environment:**
   ```
   build_with_venv.bat
   ```
2. Find the executable in the `dist` folder
3. Double-click `FindingExcellence.exe` to run (no Python installation needed)

### Option 3: Legacy Installation (Not Recommended)

1. Ensure you have Python 3.6+ installed (the application has been tested with Python 3.13.3)
2. Clone this repository or download the source code
3. Install dependencies:
   ```
   pip install -r build_resources/requirements.txt
   ```
4. Run the application:
   ```
   python main.py
   ```

**⚠️ Note:** Option 3 may have version conflicts. Use Option 1 for stable development.

## How to Use

1. **Search by Filename**:
   - Enter search keywords to find Excel files
   - Optionally add exclusion keywords to filter out unwanted results
   - Set a date range if needed
   - Click "Search for Excel Files" to start the search

2. **View Results**:
   - Results will be displayed in a table with file names, paths, and modified dates
   - Click column headers to sort results
   - Double-click any file to open it
   - Right-click for additional options (open file, open containing folder, copy path)

3. **Search File Contents**:
   - After finding files, select ones you want to search within
   - Enter content keywords in the "Content Search" section
   - Choose whether to use case-sensitive search
   - Click "Search Selected File Contents"
   - View matches in the results dialog

4. **Export Results**:
   - Use the "Export Filename Results" button to save filename search results
   - In the content results dialog, use the "Export Results" button to save content matches

## Keyboard Shortcuts

- Ctrl+Enter: Start search
- Escape: Cancel current search
- Ctrl+A: Select all results
- Ctrl+D: Deselect all results
- Ctrl+E: Export results
- Ctrl+O: Open selected file
- Ctrl+F: Open containing folder
- Ctrl+L: Focus quick filter
- F1: Show keyboard shortcuts help

## Requirements

### For Virtual Environment (Recommended)
- Python 3.8+ (tested with Python 3.13.3)
- Automatically installed in venv:
  - pandas >= 2.3.2 (latest secure version)
  - openpyxl >= 3.1.5
  - tkcalendar >= 1.6.1
  - xlrd >= 2.0.1
  - pyinstaller >= 6.15.0

### For Legacy Installation
- Python 3.6+ (tested with Python 3.13.3)
- pandas >= 1.5.0
- openpyxl >= 3.0.0
- tkcalendar >= 1.6.0
- xlrd >= 2.0.0
- pyinstaller >= 5.0.0 (for building the executable)

**Note:** Virtual environment ensures exact versions and prevents conflicts.

## Troubleshooting

### Common Issues

1. **Application doesn't start**:
   - Make sure all dependencies are installed
   - Check the log file (finding_excellence.log) for error details

2. **Search returns no results**:
   - Verify that you have Excel files in the selected folders
   - Try broader search terms or disable date filtering

3. **Content search is slow**:
   - Large Excel files take longer to search
   - Select fewer files for content searching

4. **Icons not showing in executable**:
   - This is a known issue with some PyInstaller builds
   - The application will still function correctly

### Getting Help

If you encounter any issues not covered here, please:
1. Check the log file (finding_excellence.log) for detailed error information
2. Open an issue on GitHub with the error details and steps to reproduce

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This software is provided as-is without any warranty. Consider it licensed under the MIT License.
