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
        Create folder selection components with listbox for multi-folder management.
        """
        # Label row
        label_frame = ttk.Frame(self.criteria_frame)
        label_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Label(label_frame, text="Search Folders:").pack(side=tk.LEFT, padx=5)

        # Listbox and buttons container
        container_frame = ttk.Frame(self.criteria_frame)
        container_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Listbox with scrollbars
        listbox_frame = ttk.Frame(container_frame)
        listbox_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.folders_listbox = tk.Listbox(
            listbox_frame,
            height=4,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            selectmode=tk.SINGLE,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.folders_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar.config(command=self.folders_listbox.yview)
        h_scrollbar.config(command=self.folders_listbox.xview)

        # Buttons frame
        buttons_frame = ttk.Frame(container_frame)
        buttons_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))

        ttk.Button(
            buttons_frame,
            text="Add Folder",
            command=self._add_folder,
            width=12
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            buttons_frame,
            text="Remove",
            command=self._remove_folder,
            width=12
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            buttons_frame,
            text="Reset Defaults",
            command=self._reset_default_folders,
            width=12
        ).pack(fill=tk.X, pady=2)

        # Load initial paths and populate listbox
        self.search_paths = self._load_initial_paths()
        self._populate_listbox()
    
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
    
    def _load_initial_paths(self):
        """
        Load folder paths from config or return defaults on first run.

        Returns:
            list: List of folder paths to search
        """
        saved_paths = self.config.get("search_folders", None)

        if isinstance(saved_paths, list) and len(saved_paths) > 0:
            logging.info(f"Loaded search folders from config: {saved_paths}")
            return saved_paths

        # First run or missing config: return defaults
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        defaults = [downloads_path, desktop_path]
        logging.info(f"Using default search folders: {defaults}")
        return defaults

    def _populate_listbox(self):
        """
        Populate the folders listbox from self.search_paths.
        """
        self.folders_listbox.delete(0, tk.END)
        for path in self.search_paths:
            self.folders_listbox.insert(tk.END, path)

    def _add_folder(self):
        """
        Open folder browser dialog and add selected folder to search paths.
        """
        from tkinter import filedialog

        # Determine initial directory
        initial_dir = os.path.expanduser("~")
        for path in self.search_paths:
            if os.path.isdir(path):
                initial_dir = path
                break

        folder = filedialog.askdirectory(initialdir=initial_dir)

        if not folder:
            return

        # Check for duplicates using normalized paths
        normalized_folder = os.path.normpath(folder)
        normalized_existing = [os.path.normpath(p) for p in self.search_paths]

        if normalized_folder in normalized_existing:
            messagebox.showwarning("Duplicate Folder", "This folder is already in the list.")
            return

        # Add to search paths and update UI
        self.search_paths.append(folder)
        self._populate_listbox()
        self._save_paths_to_config()
        logging.info(f"Added folder to search paths: {folder}")

    def _remove_folder(self):
        """
        Remove the selected folder from the search paths.
        """
        selection = self.folders_listbox.curselection()

        if not selection:
            messagebox.showwarning("No Selection", "Please select a folder to remove.")
            return

        idx = selection[0]
        removed = self.search_paths.pop(idx)
        self._populate_listbox()
        self._save_paths_to_config()
        logging.info(f"Removed folder from search paths: {removed}")

    def _reset_default_folders(self):
        """
        Reset search paths to the default (Downloads and Desktop).
        """
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.search_paths = [downloads_path, desktop_path]
        self._populate_listbox()
        self._save_paths_to_config()
        logging.info("Reset search folders to defaults")

    def _save_paths_to_config(self):
        """
        Save the current search paths to the configuration file.
        """
        self.config.set("search_folders", self.search_paths)
        self.config.save_config()
    
    def _search_by_filename(self):
        """
        Validate input and initiate a filename search.
        """
        # Check if a search is already running
        if self.callbacks.get('is_filename_search_active', lambda: False)():
            messagebox.showwarning("Search in Progress", "A filename search is already running.")
            return
        
        # Verify at least one folder exists
        if not self.search_paths:
            messagebox.showerror("Error", "Your folder list is empty. Please add at least one folder.")
            logging.error("Search attempt with empty folder list")
            return

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
