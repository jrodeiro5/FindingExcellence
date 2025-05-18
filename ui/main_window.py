"""
Main window UI components for the FindingExcellence application.

This module defines the primary application window and
coordinates all UI elements and interactions.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import logging
import datetime
import traceback
import sys

# Internal modules
from core.config_manager import ConfigManager
from core.file_search import FileSearch
from core.content_search import ContentSearch
from ui.search_panel import SearchPanel
from ui.results_panel import ResultsPanel
from ui.content_search_panel import ContentSearchPanel
from ui.dialogs import ContentResultsDialog
# Keyboard shortcuts temporarily disabled
from utils.export import ExportManager

class ExcelFinderApp:
    """
    Main application class that manages the Excel Finder GUI.
    """
    
    def __init__(self, root):
        """
        Initialize the main application window.
        
        Args:
            root: The Tkinter root window
        """
        self.root = root
        self.root.title("FindingExcellence")
        self.root.geometry("950x750")
        
        # Initialize state variables
        self.cancel_event = threading.Event()
        self.filename_search_active = False
        self.content_search_active = False
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        
        # Initialize search engines
        self.file_search = FileSearch(self.cancel_event)
        self.content_search = ContentSearch(self.cancel_event)
        
        # Apply UI styling
        self._setup_ui_style()
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top section for search inputs
        top_section = ttk.Frame(main_frame)
        top_section.pack(fill=tk.X, padx=5, pady=5)
        
        # Create UI components
        self._create_search_panel(top_section)
        self._create_content_search_panel(top_section)
        self._create_results_panel(main_frame)
        self._create_progress_bar()
        self._create_status_bar()
        
        # Setup keyboard shortcuts directly in main window
        self._setup_keyboard_shortcuts()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_keyboard_shortcuts(self):
        """
        Set up keyboard shortcuts for common operations.
        """
        # Search (Ctrl+Enter)
        self.root.bind('<Control-Return>', lambda e: self._trigger_search())
        
        # Cancel (Escape)
        self.root.bind('<Escape>', lambda e: self.cancel_current_search())
        
        # Select All (Ctrl+A)
        self.root.bind('<Control-a>', lambda e: self.results_panel.select_all_results())
        
        # Deselect All (Ctrl+D)
        self.root.bind('<Control-d>', lambda e: self.results_panel.deselect_all_results())
        
        # Export (Ctrl+E)
        self.root.bind('<Control-e>', lambda e: self.results_panel._export_filename_results())
        
        # Open selected file (Ctrl+O)
        self.root.bind('<Control-o>', lambda e: self.results_panel._open_selected_file())
        
        # Open containing folder (Ctrl+F)
        self.root.bind('<Control-f>', lambda e: self.results_panel._open_containing_folder())
        
        # Focus quick filter (Ctrl+L)
        self.root.bind('<Control-l>', lambda e: self._focus_quick_filter())
        
        # Show keyboard shortcuts help (F1)
        self.root.bind('<F1>', lambda e: self._show_keyboard_shortcuts())
    
    def _trigger_search(self):
        """
        Trigger a search operation with current settings.
        """
        if not self.filename_search_active:
            self.search_panel._search_by_filename()
    
    def _focus_quick_filter(self):
        """
        Set focus to the quick filter input.
        """
        for child in self.results_panel.results_frame.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.Frame):
                        for widget in subchild.winfo_children():
                            if isinstance(widget, ttk.Entry):
                                widget.focus_set()
                                return
    
    def _show_keyboard_shortcuts(self):
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
    
    def _setup_ui_style(self):
        """
        Set up the UI styling for the application.
        """
        style = ttk.Style()
        style.theme_use('clam')  # Or 'alt', 'default', 'classic'
        style.configure("TLabel", padding=3)
        style.configure("TButton", padding=3)
        style.configure("TEntry", padding=3)
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Special style for accent button
        style.configure("Accent.TButton", 
                      foreground="#ffffff",
                      background="#4a7dff",
                      relief="raised",  # 3D style
                      borderwidth=2,
                      padding=8,
                      font=('Helvetica', 10, 'bold'))
                      
        style.map("Accent.TButton",
                 foreground=[('pressed', '#ffffff'), ('active', '#ffffff'), ('disabled', '#cccccc')],
                 background=[('pressed', '#3a67d7'), ('active', '#5a8dff'), ('disabled', '#a0a0a0')],
                 relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
    
    def _create_search_panel(self, parent):
        """
        Create the search panel for filename search.
        """
        # Define callbacks for the search panel
        search_callbacks = {
            'on_filename_search': self._start_filename_search,
            'on_cancel_search': self.cancel_current_search,
            'is_filename_search_active': lambda: self.filename_search_active
        }
        
        self.search_panel = SearchPanel(parent, self.config_manager, search_callbacks)
    
    def _create_content_search_panel(self, parent):
        """
        Create the content search panel.
        """
        # Define callbacks for the content search panel
        content_search_callbacks = {
            'on_content_search': self._start_content_search,
            'get_selected_files': lambda: self.results_panel.get_selected_files(),
            'update_status': lambda msg: self.status_var.set(msg)
        }
        
        self.content_search_panel = ContentSearchPanel(parent, content_search_callbacks)
    
    def _create_results_panel(self, parent):
        """
        Create the results panel.
        """
        # Define callbacks for the results panel
        results_callbacks = {
            'on_result_selection_change': self._on_result_selection_change,
            'on_export_filename_results': self._export_filename_results,
            'update_status': lambda msg: self.status_var.set(msg)
        }
        
        self.results_panel = ResultsPanel(parent, results_callbacks)
    
    def _create_progress_bar(self):
        """
        Create the progress bar (initially hidden).
        """
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", mode="indeterminate")
        # Initially not displayed, will be shown when needed
    
    def _create_status_bar(self):
        """
        Create the status bar at the bottom of the window.
        """
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Main status message
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            status_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W, 
            padding=3
        )
        self.status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Keyboard shortcuts indicator disabled
        
        self.status_var.set("Ready. Select a folder and criteria to begin.")
    
    def _on_result_selection_change(self, selected_items):
        """
        Handle changes in the selection of results.
        """
        self.content_search_panel.update_selection_status(selected_items)
    
    def _start_progress(self, mode="indeterminate", max_val=0):
        """
        Start and display the progress bar.
        """
        # Show progress bar above status bar
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5, before=self.status_bar.master)
        
        # Configure mode
        if mode == "determinate":
            self.progress_bar.config(mode="determinate", maximum=max_val, value=0)
        else:
            self.progress_bar.config(mode="indeterminate")
            self.progress_bar.start(100)  # Speed
        
        # Force UI update
        self.root.update()
    
    def _stop_progress(self):
        """
        Stop and hide the progress bar.
        """
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        # Force UI update
        self.root.update()
    
    def _update_progress(self, value=None):
        """
        Update the progress bar value.
        """
        if self.progress_bar.cget("mode") == "determinate":
            if value is not None:
                self.progress_bar.config(value=value)
            else:  # step
                self.progress_bar.step()
        # Force UI update - lighter than update()
        self.root.update_idletasks()
    
    def cancel_current_search(self):
        """
        Cancel the current search operation.
        """
        self.status_var.set("Cancellation requested...")
        self.cancel_event.set()
        self.search_panel.set_search_buttons_state(enable=True)
        logging.info("Search cancellation requested by user.")
    
    def _toggle_search_buttons(self, enable=True):
        """
        Toggle the state of search buttons.
        """
        self.search_panel.set_search_buttons_state(enable)
        
        # If disabling for content search, also disable content search button
        if not enable and self.content_search_active:
            self.content_search_panel.set_search_button_state(enable=False)
    
    def _start_filename_search(self, folder_path, filename_keywords, start_date, end_date, 
                              exclude_keywords, case_sensitive):
        """
        Start a filename search operation.
        """
        # Reset cancellation event
        self.cancel_event.clear()
        
        # Clear previous results
        self.results_panel.clear_results()
        
        # Hide content search panel for new search
        self.content_search_panel.hide()
        
        # Update UI state
        self._toggle_search_buttons(enable=False)
        self.filename_search_active = True
        self.status_var.set("Searching filenames...")
        self._start_progress()
        
        # Log search
        folder_desc = folder_path if isinstance(folder_path, str) else ', '.join(folder_path)
        logging.info(
            f"Filename search started. Folder(s): '{folder_desc}', "
            f"Keywords: '{','.join(filename_keywords)}', "
            f"Exclude: '{','.join(exclude_keywords)}', "
            f"Dates: {start_date}-{end_date}, "
            f"CaseSensitive: {case_sensitive}"
        )

        # Start search in a separate thread
        threading.Thread(
            target=self._run_filename_search,
            args=(folder_path, filename_keywords, start_date, end_date, exclude_keywords, case_sensitive),
            daemon=True
        ).start()
    
    def _run_filename_search(self, folder_path, filename_keywords, start_date, end_date, 
                            exclude_keywords, case_sensitive):
        """
        Run the filename search in a background thread.
        """
        try:
            # Define status update callback
            def update_status(msg):
                self.root.after(0, lambda m=msg: self.status_var.set(m))
                self.root.after(0, self.root.update_idletasks)
            
            # Perform the search
            found_files = self.file_search.search_by_filename(
                folder_path,
                filename_keywords,
                start_date,
                end_date,
                exclude_keywords,
                case_sensitive,
                status_callback=update_status
            )
            
            # Update UI with results
            self.root.after(0, self._update_results_and_finalize_filename_search, 
                          found_files, self.cancel_event.is_set())
                          
        except Exception as e:
            error_message = f"Error during filename search: {str(e)}"
            self.root.after(0, lambda: self._handle_error("filename search", e))
            self.root.after(0, self._stop_progress)
            self.root.after(0, lambda: self._toggle_search_buttons(enable=True))
            self.root.after(0, lambda: setattr(self, 'filename_search_active', False))
    
    def _update_results_and_finalize_filename_search(self, files, cancelled):
        """
        Update the UI with search results and finalize the search operation.
        """
        # Add files to results
        self.results_panel.add_results(files)
        
        # Reset UI state
        self._stop_progress()
        self._toggle_search_buttons(enable=True)
        self.filename_search_active = False
        
        # Update status message
        if cancelled:
            self.status_var.set(f"Filename search cancelled. Found {len(files)} files before stopping.")
        else:
            self.status_var.set(f"Found {len(files)} files.")
            logging.info(f"Filename search completed. Found {len(files)} files.")
        
        # Show content search panel if files found
        if files:
            # Auto-select all files if not too many
            if len(files) <= 20:
                self.results_panel.select_all_results()
                self.status_var.set(f"Found {len(files)} files. All selected and ready for content search.")
            
            # Force update before next phase
            self.root.update()
            
            # Show content search panel
            self.content_search_panel.show(after_widget=self.search_panel.criteria_frame)
            
            # Adjust window size if needed
            current_height = self.root.winfo_height()
            if current_height < 800:
                self.root.geometry(f"950x800")
            
            # Special message for many files
            if len(files) > 20:
                messagebox.showinfo(
                    "Many Files Found",
                    f"Found {len(files)} files. Please select specific files for content search, "
                    f"or use 'Select All' if you want to search all of them."
                )
        else:
            # Hide content search panel if no results
            self.content_search_panel.hide()
        
        # Final UI update
        self.root.update()
    
    def _start_content_search(self, files_to_search, keywords, case_sensitive):
        """
        Start a content search operation.
        """
        # Reset cancellation event
        self.cancel_event.clear()
        
        # Update UI state
        self._toggle_search_buttons(enable=False)
        self.content_search_panel.set_search_button_state(enable=False)
        self.content_search_active = True
        
        # Update status
        self.status_var.set(f"Starting content search in {len(files_to_search)} files...")
        self._start_progress(mode="determinate", max_val=len(files_to_search))
        
        # Log search
        logging.info(
            f"Content search started for {len(files_to_search)} files. "
            f"Keywords: '{','.join(keywords)}', "
            f"CaseSensitive: {case_sensitive}"
        )
        
        # Start search in a separate thread
        threading.Thread(
            target=self._run_content_search,
            args=(files_to_search, keywords, case_sensitive),
            daemon=True
        ).start()
    
    def _run_content_search(self, files_to_search, keywords, case_sensitive):
        """
        Run the content search in a background thread.
        """
        try:
            # Define progress callback
            def update_progress(current, total):
                self.root.after(0, self._update_progress, current)
                self.root.after(
                    0, 
                    lambda c=current, t=total: self.status_var.set(
                        f"Content search: Processed {c}/{t} files..."
                    )
                )
            
            # Perform the search
            all_results = self.content_search.search_files_contents(
                files_to_search,
                keywords,
                case_sensitive,
                progress_callback=update_progress
            )
            
            # Update UI with results
            self.root.after(0, self._finalize_content_search, all_results, self.cancel_event.is_set())
            
        except Exception as e:
            self.root.after(0, lambda: self._handle_error("content search", e))
            self.root.after(0, self._stop_progress)
            self.root.after(0, lambda: self._toggle_search_buttons(enable=True))
            self.root.after(0, lambda: self.content_search_panel.set_search_button_state(enable=True))
            self.root.after(0, lambda: setattr(self, 'content_search_active', False))
    
    def _finalize_content_search(self, all_results, cancelled):
        """
        Finalize the content search and display results.
        """
        # Reset UI state
        self._stop_progress()
        self._toggle_search_buttons(enable=True)
        self.content_search_panel.set_search_button_state(enable=True)
        self.content_search_active = False
        
        # Update status
        if cancelled:
            self.status_var.set("Content search cancelled. Processed results shown.")
        else:
            self.status_var.set("Content search completed.")
            logging.info("Content search completed.")
        
        # Show results
        if not all_results and not cancelled:
            messagebox.showinfo("No Matches", "No content matches found in the selected files for the given keywords.")
        elif all_results:
            # Show results dialog
            ContentResultsDialog(
                self.root, 
                all_results, 
                export_callback=self._export_content_results
            )
    
    def _export_filename_results(self, result_items):
        """
        Export filename search results to a file.
        """
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Export Filename Search Results"
        )
        
        if not filepath:
            return
        
        # Extract values from treeview items
        results = []
        for item_id in result_items:
            results.append(self.results_panel.results_tree.item(item_id, 'values'))
        
        # Export using ExportManager
        success = ExportManager.export_filename_results(results, filepath)
        
        if success:
            messagebox.showinfo("Export Successful", f"Results exported to {filepath}")
        else:
            messagebox.showerror("Export Error", "Could not export results. See log for details.")
    
    def _export_content_results(self, results_map, parent_window):
        """
        Export content search results to a file.
        """
        if not results_map:
            messagebox.showinfo("No Results", "No content results to export.", parent=parent_window)
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",  # Text format for better readability
            filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Content Search Results",
            parent=parent_window  # Ensure dialog is on top of results window
        )
        
        if not filepath:
            return
        
        # Export using ExportManager
        success = ExportManager.export_content_results(results_map, filepath)
        
        if success:
            messagebox.showinfo("Export Successful", f"Content results exported to {filepath}", parent=parent_window)
        else:
            messagebox.showerror("Export Error", "Could not export content results. See log for details.", parent=parent_window)
    
    def _on_closing(self):
        """
        Handle the window close event.
        """
        if self.filename_search_active or self.content_search_active:
            if messagebox.askyesno(
                "Confirm Exit", 
                "A search is currently active. Are you sure you want to exit? "
                "This will try to cancel the search."
            ):
                self.cancel_event.set()  # Signal cancellation
                # Give a moment for threads to potentially see the cancel event
                self.root.after(100, self._shutdown_app)
            else:
                return  # Don't close
        else:
            self._shutdown_app()
    
    def _shutdown_app(self):
        """
        Properly shut down the application.
        """
        logging.info("Application shutting down.")
        
        # Gracefully shut down content search executor
        self.content_search.shutdown()
        
        # Save configuration
        self.config_manager.save_config()
        
        # Close the window
        self.root.destroy()
        
    def _handle_error(self, operation, error, show_message=True):
        """
        Handle errors uniformly throughout the application.
        
        Args:
            operation: String describing the operation that failed
            error: The exception that was raised
            show_message: Whether to show a message box to the user
        """
        # Get the full traceback
        tb = traceback.format_exc()
        
        # Log the error
        logging.error(f"Error during {operation}: {error}\n{tb}")
        
        # Show message box if requested
        if show_message:
            messagebox.showerror(
                "Operation Error",
                f"An error occurred during {operation}: {error}\n\n"
                f"The error has been logged."
            )
        
        # Return False to indicate failure
        return False