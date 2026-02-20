# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FindingExcellence is a desktop GUI application for searching Excel files by filename and content. Built with Python and Tkinter, it provides fast file discovery and content searching across Desktop and Downloads folders with support for .xls, .xlsx, and .xlsm formats.

## Build and Development Commands

### Setup and Installation
```bash
# Option 1: Create and activate virtual environment (Recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies (if not using a pre-configured venv)
pip install -r build_resources/requirements.txt

# Run the application
python main.py
```

### Running Tests
Tests are located in the `test/` directory. Run tests with:
```bash
# Run all tests
python -m pytest test/

# Run a specific test file
python -m pytest test/test_search_improvements.py

# Run with verbose output
python -m pytest test/ -v
```

### Building Executable
```bash
# Build with isolated virtual environment (recommended for distribution)
build_with_venv.bat

# Find the executable in the dist/ folder
# Output: FindingExcellence.exe (no Python installation required to run)
```

### Linting and Code Quality
No formal linting configuration is in place. Use standard Python conventions (PEP 8).

## Architecture Overview

### Core Components

**1. Search Engine (`core/` module)**
- **`file_search.py`**: Filename-based searching with filtering by date range, keywords, exclusions, and case sensitivity
- **`content_search.py`**: Parallel content searching within selected files using ThreadPoolExecutor with configurable worker threads (default: cpu_count // 2)
- **`excel_processor.py`**: Multi-strategy Excel file reading supporting .xls (xlrd), .xlsx and .xlsm (openpyxl, pandas), with diagnostics and fallback handling
- **`config_manager.py`**: JSON-based configuration persistence for user preferences

**2. User Interface (`ui/` module)**
- **`main_window.py`**: Main application orchestrator that manages keyboard shortcuts (Ctrl+Enter search, Esc cancel, Ctrl+A/D select), event threading, and component coordination
- **`search_panel.py`**: Search input fields and filename search controls
- **`results_panel.py`**: Results table with sorting, selection, and export capabilities
- **`content_search_panel.py`**: Content search controls and case-sensitivity options
- **`dialogs.py`**: Modal dialogs for content results display and user interactions

**3. Utilities (`utils/` module)**
- **`export.py`**: CSV/text export functionality
- **`logging_setup.py`**: Centralized logging to `finding_excellence.log`

### Data Flow

1. **Filename Search**: User input → FileSearch → results in memory → displayed in ResultsPanel
2. **Content Search**: Selected files → ContentSearch (parallel processing) → matches grouped by file → displayed in dialog
3. **Configuration**: ConfigManager loads/saves to `finding_excellence_config.json`

### Key Design Patterns

- **Threading Events**: `cancel_event` passed through search classes for responsive cancellation
- **Callbacks**: Progress callbacks in search operations update UI without blocking
- **Multi-strategy Fallback**: ExcelProcessor tries multiple approaches to read corrupted/unusual Excel files
- **Thread Pool**: ContentSearch uses concurrent.futures for parallel file processing

## Development Notes

### Threading Considerations
- Main UI runs on Tkinter's event loop
- Searches execute in background threads triggered by UI events
- `cancel_event` is a threading.Event used to signal cancellation requests
- Progress callbacks allow updates without UI blocking

### Excel Processing
- **Supported formats**: .xls, .xlsx, .xlsm
- **xlrd** library required for .xls (legacy Excel)
- **openpyxl** for modern Excel files
- **pandas** used as a higher-level interface
- ExcelProcessor includes diagnostic logging for troubleshooting file read failures

### Configuration
- User preferences stored in `finding_excellence_config.json`
- ConfigManager handles persistence and defaults

### PyInstaller Packaging
- When running as executable, PyInstaller extracts to temp folder (`sys._MEIPASS`)
- Icon loading handles both script and executable contexts
- See `FindingExcellence.spec` for build configuration

## Important File Locations

- **Entry point**: `main.py`
- **Virtual environment**: `venv/` (created during setup)
- **Build output**: `dist/FindingExcellence.exe`
- **Configuration**: `finding_excellence_config.json`
- **Logs**: `finding_excellence.log`
- **Assets**: `resources/`, `build_resources/`
