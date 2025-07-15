"""
Keyboard shortcuts handling for the FindingExcellence application.

This module sets up and handles keyboard shortcuts for the application.
"""

import tkinter as tk
from tkinter import ttk

class KeyboardShortcutsManager:
    """
    Manages keyboard shortcuts for the application.
    """
    
    def __init__(self, root, app):
        """
        Initialize the keyboard shortcuts manager.
        
        Args:
            root: The Tkinter root window
            app: The main application instance
        """
        self.root = root
        self.app = app
        
        # Set up keyboard shortcuts
        self._setup_shortcuts()
    
    def _setup_shortcuts(self):
        """
        Set up all keyboard shortcuts.
        """
        # Safe setup - checking if attributes exist before binding
        # Search (Ctrl+Enter)
        if hasattr(self.app, 'search_panel'):
            self.root.bind('<Control-Return>', lambda e: self._trigger_search())
        
        # Cancel (Escape)
        self.root.bind('<Escape>', lambda e: self._cancel_search())
        
        # Select All (Ctrl+A)
        if hasattr(self.app, 'results_panel'):
            self.root.bind('<Control-a>', lambda e: self._select_all())
        
        # Deselect All (Ctrl+D)
        if hasattr(self.app, 'results_panel'):
            self.root.bind('<Control-d>', lambda e: self._deselect_all())
        
        # Export (Ctrl+E)
        if hasattr(self.app, 'results_panel'):
            self.root.bind('<Control-e>', lambda e: self._export_results())
        
        # Open selected file (Ctrl+O)
        if hasattr(self.app, 'results_panel'):
            self.root.bind('<Control-o>', lambda e: self._open_selected())
        
        # Open containing folder (Ctrl+F)
        if hasattr(self.app, 'results_panel'):
            self.root.bind('<Control-f>', lambda e: self._open_folder())
        
        # Focus quick filter (Ctrl+L)
        self.root.bind('<Control-l>', lambda e: self._focus_filter())
        
        # Show keyboard shortcuts help (F1)
        self.root.bind('<F1>', lambda e: self.show_keyboard_shortcuts())
    
    def _trigger_search(self):
        """Safely trigger a search operation."""
        if hasattr(self.app, 'search_panel') and hasattr(self.app.search_panel, '_search_by_filename'):
            if not getattr(self.app, 'filename_search_active', True):
                self.app.search_panel._search_by_filename()
    
    def _cancel_search(self):
        """Safely cancel current search."""
        if hasattr(self.app, 'cancel_current_search'):
            self.app.cancel_current_search()
    
    def _select_all(self):
        """Safely select all results."""
        if hasattr(self.app, 'results_panel') and hasattr(self.app.results_panel, 'select_all_results'):
            self.app.results_panel.select_all_results()
    
    def _deselect_all(self):
        """Safely deselect all results."""
        if hasattr(self.app, 'results_panel') and hasattr(self.app.results_panel, 'deselect_all_results'):
            self.app.results_panel.deselect_all_results()
    
    def _export_results(self):
        """Safely export results."""
        if hasattr(self.app, 'results_panel') and hasattr(self.app.results_panel, '_export_filename_results'):
            self.app.results_panel._export_filename_results()
    
    def _open_selected(self):
        """Safely open selected file."""
        if hasattr(self.app, 'results_panel') and hasattr(self.app.results_panel, '_open_selected_file'):
            self.app.results_panel._open_selected_file()
    
    def _open_folder(self):
        """Safely open containing folder."""
        if hasattr(self.app, 'results_panel') and hasattr(self.app.results_panel, '_open_containing_folder'):
            self.app.results_panel._open_containing_folder()
    
    def _focus_filter(self):
        """Safely focus on quick filter if available."""
        # First try to access the filter in results panel
        if hasattr(self.app, 'results_panel'):
            for widget in self.app.results_panel.results_frame.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Entry):
                            child.focus_set()
                            return
    
    def show_keyboard_shortcuts(self):
        """
        Display a dialog with keyboard shortcuts information.
        """
        shortcuts = {
            "Ctrl+Enter": "Start search",
            "Escape": "Cancel current search",
            "Ctrl+A": "Select all results",
            "Ctrl+D": "Deselect all results",
            "Ctrl+E": "Export results",
            "Ctrl+O": "Open selected file",
            "Ctrl+F": "Open containing folder",
            "Ctrl+L": "Focus quick filter",
            "F1": "Show this help"
        }
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Keyboard Shortcuts")
        dialog.geometry("400x300")
        dialog.transient(self.root)  # Stay on top of main window
        dialog.grab_set()  # Modal dialog
        
        # Add shortcuts list
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Keyboard Shortcuts", font=("Helvetica", 12, "bold")).pack(pady=(0, 10))
        
        # Create a frame for the shortcuts list
        shortcuts_frame = ttk.Frame(frame)
        shortcuts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add column headers
        ttk.Label(shortcuts_frame, text="Shortcut", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(shortcuts_frame, text="Action", font=("Helvetica", 10, "bold")).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Add separator
        ttk.Separator(shortcuts_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=5)
        
        # Add shortcuts
        for i, (shortcut, description) in enumerate(shortcuts.items(), start=2):
            ttk.Label(shortcuts_frame, text=shortcut).grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            ttk.Label(shortcuts_frame, text=description).grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Close button
        ttk.Button(frame, text="Close", command=dialog.destroy).pack(pady=(10, 0))
