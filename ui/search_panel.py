"""
Search panel UI components.

This module contains UI elements for search criteria input.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import datetime
import logging
from ui.dialogs import CalendarDialog

class SearchPanel:
    """
    Panel for entering search criteria (filename, date range, etc.).
    """
    
    def __init__(self, parent, config_manager, callbacks):
        """
        Initialize the search panel.
        
        Args:
            parent: Parent frame/widget
            config_manager: Configuration manager object
            callbacks: Dictionary of callback functions
        """
        self.parent = parent
        self.config = config_manager
        self.callbacks = callbacks
        
        # Create the search criteria frame
        self.criteria_frame = ttk.LabelFrame(parent, text="Search Criteria", padding="10")
        self.criteria_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create the search UI components
        self._create_folder_selection()
        self._create_filename_search_options()
        self._create_date_range_selectors()
        self._create_exclude_keywords()
        self._create_search_buttons()
    
    def _create_folder_selection(self):
        """
        Create folder selection components.
        """
        folder_frame = ttk.Frame(self.criteria_frame)
        folder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(folder_frame, text="Folder:").pack(side=tk.LEFT, padx=5)
        
        # Get default search paths - both Downloads and Desktop
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # Initialize with Downloads as visible path
        self.folder_path = tk.StringVar(value=downloads_path)
        
        # Store actual search paths (will include both Downloads and Desktop)
        self.search_paths = [downloads_path, desktop_path]
        
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=60)
        folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(folder_frame, text="Browse", 
                               command=self._browse_folder)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Add a label indicating that both folders are searched
        ttk.Label(folder_frame, text="(Searching in both Downloads and Desktop)", 
                 font=("Helvetica", 8, "italic")).pack(side=tk.LEFT, padx=5)
    
    def _create_filename_search_options(self):
        """
        Create filename search options.
        """
        filename_options_frame = ttk.Frame(self.criteria_frame)
        filename_options_frame.pack(fill=tk.X, pady=5)
        
        filename_frame = ttk.Frame(filename_options_frame)
        filename_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(filename_frame, text="Filename Keywords (Excel files, comma-separated):").pack(side=tk.LEFT, padx=5)
        
        self.filename_keywords = tk.StringVar()
        filename_entry = ttk.Entry(filename_frame, textvariable=self.filename_keywords, width=50)
        filename_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.filename_case_sensitive = tk.BooleanVar(value=False)
        filename_case_checkbox = ttk.Checkbutton(
            filename_options_frame, 
            text="Case Sensitive", 
            variable=self.filename_case_sensitive
        )
        filename_case_checkbox.pack(side=tk.LEFT, padx=10)
    
    def _create_date_range_selectors(self):
        """
        Create date range selection components.
        """
        date_frame = ttk.Frame(self.criteria_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        # Start date
        ttk.Label(date_frame, text="Start Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.start_date_var = tk.StringVar()
        self.start_date_entry = ttk.Entry(date_frame, width=12, textvariable=self.start_date_var)
        self.start_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            date_frame, 
            text="Select", 
            command=lambda: self._show_calendar(self.start_date_var)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            date_frame, 
            text="Clear", 
            command=lambda: self.start_date_var.set("")
        ).pack(side=tk.LEFT, padx=2)
        
        # End date
        ttk.Label(date_frame, text="End Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=(15,5))
        self.end_date_var = tk.StringVar()
        self.end_date_entry = ttk.Entry(date_frame, width=12, textvariable=self.end_date_var)
        self.end_date_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            date_frame, 
            text="Select", 
            command=lambda: self._show_calendar(self.end_date_var)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            date_frame, 
            text="Clear", 
            command=lambda: self.end_date_var.set("")
        ).pack(side=tk.LEFT, padx=2)
    
    def _create_exclude_keywords(self):
        """
        Create exclude keywords component.
        """
        exclude_frame = ttk.Frame(self.criteria_frame)
        exclude_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(exclude_frame, text="Exclude Keywords (comma-separated):").pack(side=tk.LEFT, padx=5)
        
        self.exclude_keywords = tk.StringVar()
        exclude_entry = ttk.Entry(exclude_frame, textvariable=self.exclude_keywords, width=50)
        exclude_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def _create_search_buttons(self):
        """
        Create search and cancel buttons.
        """
        button_frame = ttk.Frame(self.criteria_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.filename_search_btn = ttk.Button(
            button_frame, 
            text="Search by Filename", 
            command=self._search_by_filename
        )
        self.filename_search_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(
            button_frame, 
            text="Cancel Search", 
            command=self._cancel_search,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=15)
    
    def _show_calendar(self, string_var):
        """
        Show the calendar dialog for date selection.
        
        Args:
            string_var: StringVar to store the selected date
        """
        CalendarDialog(self.parent.winfo_toplevel(), string_var)
    
    def _browse_folder(self):
        """
        Open folder browser dialog and update folder path display, while maintaining Desktop in search paths.
        """
        from tkinter import filedialog
        
        initial_dir = self.folder_path.get() if os.path.isdir(self.folder_path.get()) else os.path.expanduser("~")
        folder = filedialog.askdirectory(initialdir=initial_dir)
        
        if folder:
            # Update the displayed folder path
            self.folder_path.set(folder)
            
            # Make sure our search paths includes this folder and Desktop
            self.search_paths = [folder]
            
            # Add Desktop to search paths if it's not already the selected folder
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            if os.path.normpath(folder) != os.path.normpath(desktop_path):
                self.search_paths.append(desktop_path)
                
            # Same for Downloads folder
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            if os.path.normpath(folder) != os.path.normpath(downloads_path):
                self.search_paths.append(downloads_path)
                
            logging.info(f"Updated search paths to: {self.search_paths}")
            self.config.set("last_folder", folder)
            self.config.save_config()
    
    def _search_by_filename(self):
        """
        Validate input and initiate a filename search.
        """
        # Check if a search is already running
        if self.callbacks.get('is_filename_search_active', lambda: False)():
            messagebox.showwarning("Search in Progress", "A filename search is already running.")
            return
        
        # Use the combined search paths (Downloads and Desktop)
        # Verify at least one folder exists
        valid_paths = [path for path in self.search_paths if os.path.isdir(path)]
        if not valid_paths:
            messagebox.showerror("Error", "No valid search folders found.")
            logging.error(f"Search attempt with no valid folders: {self.search_paths}")
            return
        
        # Get search parameters
        filename_kws_str = self.filename_keywords.get()
        filename_keywords = [kw.strip() for kw in filename_kws_str.split(',') if kw.strip()]
        
        exclude_kws_str = self.exclude_keywords.get()
        exclude_keywords = [kw.strip() for kw in exclude_kws_str.split(',') if kw.strip()]
        
        case_sensitive = self.filename_case_sensitive.get()
        
        # Parse date range
        start_date, end_date = None, None
        try:
            start_date_str = self.start_date_var.get().strip()
            end_date_str = self.end_date_var.get().strip()
            
            if start_date_str:
                start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
                
            if end_date_str:
                end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
                
            # Verify date range if both dates provided
            if start_date and end_date and end_date < start_date:
                messagebox.showerror("Date Error", "End date cannot be before start date.")
                return
        except ValueError:
            messagebox.showerror("Date Error", "Invalid date format. Please use YYYY-MM-DD format.")
            return
        except Exception as e:
            messagebox.showerror("Date Error", f"Error with date input: {e}")
            return
        
        # Initiate search via callback
        if 'on_filename_search' in self.callbacks:
            self.callbacks['on_filename_search'](
                self.search_paths, 
                filename_keywords, 
                start_date, 
                end_date, 
                exclude_keywords, 
                case_sensitive
            )
    
    def _cancel_search(self):
        """
        Cancel the current search operation.
        """
        if 'on_cancel_search' in self.callbacks:
            self.callbacks['on_cancel_search']()
    
    def set_search_buttons_state(self, enable=True):
        """
        Enable or disable search buttons.
        
        Args:
            enable: True to enable, False to disable
        """
        state = tk.NORMAL if enable else tk.DISABLED
        self.filename_search_btn.config(state=state)
        
        # Cancel button state is inverse of search button
        self.cancel_btn.config(state=tk.DISABLED if enable else tk.NORMAL)
