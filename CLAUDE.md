# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FindingExcellence is a desktop GUI application for searching Excel files by filename and content. Built with Python and Tkinter, it provides fast file discovery and content searching across Desktop and Downloads folders with support for .xls, .xlsx, and .xlsm formats.

## Build and Development Commands

### Quick Start (Recommended)

**For Developers:**
```bash
# Windows Command Prompt:
dev.bat

# OR bash/Git Bash:
bash start.sh
```
This creates/reuses a `venv/`, installs dependencies, and launches the app in one command. No manual setup needed.

**For Distribution Builds:**
```bash
build_dist.bat
```
This creates an isolated `build_venv/`, installs all dependencies, and produces the executable in `dist/`. No Python installation required to run the built exe.

### Manual Setup (if needed)
```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r build_resources/requirements.txt

# Run the application
python main.py
```

### Building Executable
```bash
# Recommended: use build_dist.bat (handles venv, dependencies, PyInstaller)
build_dist.bat

# OR manual:
python -m venv build_venv
build_venv\Scripts\activate
pip install -r build_resources/requirements.txt pyinstaller>=6.15.0
python -m PyInstaller build_resources\FindingExcellence.spec --distpath=dist --workpath=build --clean
```

The executable is produced in `dist/FindingExcellence/` and requires no Python installation to run.

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

## UI Component Interactions

The main window (`ui/main_window.py`) orchestrates all UI components:
- **SearchPanel**: Handles filename search filters (keywords, exclusions, date range)
- **ResultsPanel**: Displays filename search results in a sortable table
- **ContentSearchPanel**: Controls content search on selected files
- **ContentResultsDialog**: Modal dialog showing content search matches grouped by file

All components communicate through the main application instance using callbacks and events.

## Threading Model

The application uses a `cancel_event` (threading.Event) for responsive cancellation:
- Passed to FileSearch and ContentSearch classes
- Checked during long-running operations to allow user cancellation
- Set when user clicks cancel button or presses Escape
- Critical for maintaining UI responsiveness during searches

Search operations run in background threads while UI remains responsive.

## Keyboard Shortcuts

Key shortcuts implemented in the UI:
- **Ctrl+Enter**: Start filename search
- **Escape**: Cancel current search
- **Ctrl+A**: Select all results
- **Ctrl+D**: Deselect all results
- **Ctrl+E**: Export results
- **Ctrl+O**: Open selected file
- **Ctrl+F**: Open containing folder
- **Ctrl+L**: Focus quick filter
- **F1**: Show keyboard shortcuts help

## Important File Locations

- **Entry point**: `main.py`
- **Virtual environment**: `venv/` (created during setup)
- **Build output**: `dist/FindingExcellence.exe`
- **Configuration**: `finding_excellence_config.json`
- **Logs**: `finding_excellence.log`
- **Assets**: `resources/`, `build_resources/`
