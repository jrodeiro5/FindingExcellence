# FindingExcellence

A powerful tool for finding and searching content within Excel files in your Desktop and Downloads folders.

![FindingExcellence Logo](resources/app_icon.svg)

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

### Option 1: Run as a Python Script (Development)

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

### Option 2: Build and Run as an Executable (Recommended for End Users)

1. Run the installer script:
   ```
   install_executable.bat
   ```
   The script will automatically try to find your Python installation or prompt you to provide the path.

2. After building, find the executable in the `dist` folder
3. Double-click `FindingExcellence.exe` to run the application (no Python installation needed)

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

- Python 3.6+ (tested with Python 3.13.3)
- pandas >= 1.5.0
- openpyxl >= 3.0.0
- tkcalendar >= 1.6.0
- xlrd >= 2.0.0
- pyinstaller >= 5.0.0 (for building the executable)

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
