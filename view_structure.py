"""
FindingExcellence Directory Structure Viewer

This script shows the key files and directory structure of the application.
Run this script directly to see the structure.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import subprocess

def get_tree_string(directory, prefix='', depth=0, max_depth=3, include_patterns=None, exclude_patterns=None):
    """Get a string representation of a directory tree with only the key files."""
    if include_patterns is None:
        include_patterns = ['.py', '.md', '.ico', '.svg', '.bat', '.txt', '.json']
    
    if exclude_patterns is None:
        exclude_patterns = ['__pycache__', '.pyc', '.bak', '.git', '.vscode', '.idea', 'build', 'dist']
    
    result = []
    
    if depth > max_depth:
        result.append(f"{prefix}...")
        return '\n'.join(result)
    
    try:
        items = sorted(os.listdir(directory))
        
        # Filter out excluded patterns
        filtered_items = []
        for item in items:
            if not any(excl in item for excl in exclude_patterns):
                if os.path.isdir(os.path.join(directory, item)) or any(item.endswith(incl) for incl in include_patterns):
                    filtered_items.append(item)
        
        for i, item in enumerate(filtered_items):
            item_path = os.path.join(directory, item)
            
            # Determine the prefix for the current item
            is_last = i == len(filtered_items) - 1
            item_prefix = '└── ' if is_last else '├── '
            
            # Add the current item to the result
            result.append(f"{prefix}{item_prefix}{item}")
            
            # If it's a directory, recursively process its contents
            if os.path.isdir(item_path):
                next_prefix = prefix + ('    ' if is_last else '│   ')
                result.append(get_tree_string(item_path, next_prefix, depth + 1, max_depth, include_patterns, exclude_patterns))
    
    except PermissionError:
        result.append(f"{prefix}├── [Permission denied]")
    except FileNotFoundError:
        result.append(f"{prefix}├── [Directory does not exist]")
    
    return '\n'.join(result)

def get_key_files_information():
    """Get information about key files in the application."""
    key_files_info = """
===== Key Directories =====
- core/            : Core functionality and business logic
- ui/              : User interface components
- utils/           : Utility functions and helpers
- resources/       : Application resources (icons, etc.)
- build_resources/ : Resources for building the executable

===== Key Files =====
- main.py                         : Main entry point
- core/file_search.py             : File searching functionality
- core/content_search.py          : Content searching functionality
- core/excel_processor.py         : Excel file processing
- ui/main_window.py               : Main application window
- ui/search_panel.py              : Filename search panel
- ui/content_search_panel.py      : Content search panel
- ui/results_panel.py             : Results display panel
- utils/logging_setup.py          : Logging configuration
- utils/export.py                 : Export functionality
- resources/icon.ico              : Application icon
"""
    return key_files_info

def show_gui():
    """Show the directory structure in a GUI."""
    root = tk.Tk()
    root.title("FindingExcellence Directory Structure")
    root.geometry("800x600")
    
    # Configure style
    style = ttk.Style()
    style.configure("TFrame", padding=10)
    style.configure("TLabel", padding=5, font=("Arial", 11))
    style.configure("Header.TLabel", font=("Arial", 12, "bold"))
    
    # Create main frame
    main_frame = ttk.Frame(root, style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Add header
    header_label = ttk.Label(
        main_frame, 
        text="FindingExcellence Application Structure", 
        style="Header.TLabel"
    )
    header_label.pack(fill=tk.X, pady=(0, 10))
    
    # Add intro text
    intro_label = ttk.Label(
        main_frame, 
        text="This window shows the key files and directory structure of the FindingExcellence application.",
        wraplength=750
    )
    intro_label.pack(fill=tk.X, pady=(0, 10))
    
    # Add directory tree
    tree_frame = ttk.LabelFrame(main_frame, text="Directory Structure")
    tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    # Get directory tree string
    root_dir = os.path.dirname(os.path.abspath(__file__))
    tree_string = os.path.basename(root_dir) + "\n" + get_tree_string(root_dir, '  ', 0, 2)
    
    # Create scrolled text widget for directory tree
    tree_text = scrolledtext.ScrolledText(tree_frame, width=80, height=20, font=("Courier New", 10))
    tree_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    tree_text.insert(tk.END, tree_string)
    tree_text.config(state=tk.DISABLED)
    
    # Add key files information
    info_frame = ttk.LabelFrame(main_frame, text="Key Files and Directories")
    info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    # Create scrolled text widget for key files information
    info_text = scrolledtext.ScrolledText(info_frame, width=80, height=15, font=("Courier New", 10))
    info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    info_text.insert(tk.END, get_key_files_information())
    info_text.config(state=tk.DISABLED)
    
    # Add close button
    close_button = ttk.Button(main_frame, text="Close", command=root.destroy)
    close_button.pack(pady=10)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    show_gui()
