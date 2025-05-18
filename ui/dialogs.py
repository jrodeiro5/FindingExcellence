"""
Dialog boxes for the FindingExcellence application.

This module defines various dialog boxes used throughout the application,
such as the calendar date selector and content search results.
"""

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import os

class CalendarDialog:
    """
    Dialog for selecting dates from a calendar widget.
    """
    
    def __init__(self, parent, string_var):
        """
        Initialize the calendar dialog.
        
        Args:
            parent: Parent window
            string_var: StringVar to store the selected date
        """
        self.parent = parent
        self.string_var = string_var
        self.result = None
        
        # Create dialog window
        self.top = tk.Toplevel(parent)
        self.top.title("Select Date")
        self.top.grab_set()  # Make dialog modal
        self.top.resizable(False, False)  # Prevent resizing
        
        # Position window relative to parent
        self.top.geometry(f"+{parent.winfo_rootx()+50}+{parent.winfo_rooty()+50}")
        
        # Create calendar widget
        self.cal = Calendar(self.top, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(padx=10, pady=10)
        
        # Buttons
        button_frame = ttk.Frame(self.top)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(button_frame, text="Select", command=self._select_date).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side=tk.RIGHT, padx=10)
    
    def _select_date(self):
        """
        Set the selected date and close the dialog.
        """
        date_selected = self.cal.get_date()  # Format yyyy-mm-dd
        self.string_var.set(date_selected)
        self.result = date_selected
        self.top.destroy()

class ContentResultsDialog:
    """
    Dialog for displaying content search results.
    """
    
    def __init__(self, parent, results_map, export_callback=None):
        """
        Initialize the content results dialog.
        
        Args:
            parent: Parent window
            results_map: Dictionary mapping file paths to search results
            export_callback: Function to call when exporting results
        """
        self.parent = parent
        self.results_map = results_map
        self.export_callback = export_callback
        
        # Create dialog window
        self.window = tk.Toplevel(parent)
        self.window.title("Content Search Results")
        self.window.geometry("900x700")
        self.window.transient(parent)  # Keep on top of main window
        self.window.grab_set()  # Modal behavior
        
        self._create_widgets()
    
    def _create_widgets(self):
        """
        Create the dialog widgets.
        """
        # Top bar with buttons
        top_bar = ttk.Frame(self.window)
        top_bar.pack(fill=tk.X, padx=10, pady=5)
        
        # Export button
        if self.export_callback:
            ttk.Button(
                top_bar, 
                text="Export These Results",
                command=lambda: self.export_callback(self.results_map, self.window)
            ).pack(side=tk.LEFT)
        
        # Close button
        ttk.Button(top_bar, text="Close", command=self.window.destroy).pack(side=tk.RIGHT)
        
        # Text widget for displaying results
        text_frame = ttk.Frame(self.window, padding="5")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = tk.Text(
            text_frame, 
            wrap=tk.WORD, 
            width=100, 
            height=35, 
            font=("Courier New", 9)
        )
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        h_scroll = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        self.text_widget.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self._configure_text_tags()
        
        # Insert results content
        self._display_results()
        
        # Make text widget read-only
        self.text_widget.configure(state=tk.DISABLED)
    
    def _configure_text_tags(self):
        """
        Configure text tags for styling the results display.
        """
        try:
            # Basic text styles
            self.text_widget.tag_configure("file_header_bold", font=('Helvetica', 11, 'bold'))
            self.text_widget.tag_configure("file_path_italic", font=('Helvetica', 9, 'italic'), foreground="gray40")
            self.text_widget.tag_configure("keyword_bold", font=('Courier New', 9, 'bold'), foreground="blue")
            self.text_widget.tag_configure("sheet_italic", font=('Courier New', 9, 'italic'))
            self.text_widget.tag_configure("cell_bold", font=('Courier New', 9, 'bold'))
            self.text_widget.tag_configure("value_text", font=('Courier New', 9))
            self.text_widget.tag_configure("bullet_point", font=('Courier New', 9))
            self.text_widget.tag_configure("separator", foreground="gray70")
            self.text_widget.tag_configure("summary_bold", font=('Helvetica', 10, 'bold'))
            self.text_widget.tag_configure("error_text_red", foreground="red", font=('Courier New', 9, 'bold'))
        except Exception as e:
            import logging
            logging.error(f"Error configuring text tags: {e}")
            # Fallback to basic tags if there's an error
            self.text_widget.tag_configure("file_header_bold", font=('Helvetica', 10, 'bold'))
            self.text_widget.tag_configure("error_text_red", foreground="red")
    
    def _display_results(self):
        """
        Display search results in the text widget.
        """
        try:
            if not self.results_map:
                self.text_widget.insert(tk.END, "No matches found or search was cancelled before finding results.")
                return
                
            total_matches_count = 0
            files_with_matches = 0
            
            # Process each file's results
            for file_path, findings in self.results_map.items():
                try:
                    # Check for error entry
                    if len(findings) == 1 and 'error' in findings[0]:
                        self.text_widget.insert(tk.END, f"File: {os.path.basename(file_path)}\n", "file_header_bold")
                        self.text_widget.insert(tk.END, f"Path: {file_path}\n", "file_path_italic")
                        self.text_widget.insert(tk.END, f"  ERROR: {findings[0]['error']}\n\n", "error_text_red")
                        continue

                    # Process files with findings
                    if findings:  # Ensure there are actual findings
                        files_with_matches += 1
                        self.text_widget.insert(tk.END, f"File: {os.path.basename(file_path)}\n", "file_header_bold")
                        self.text_widget.insert(tk.END, f"Path: {file_path}\n\n", "file_path_italic")
                        
                        # Display each finding
                        for finding in findings:
                            total_matches_count += 1
                            self.text_widget.insert(tk.END, f"  • Keyword '", "bullet_point")
                            self.text_widget.insert(tk.END, f"{finding['keyword']}", "keyword_bold")
                            self.text_widget.insert(tk.END, f"' found in Sheet '", "bullet_point")
                            self.text_widget.insert(tk.END, f"{finding['sheet']}", "sheet_italic")
                            self.text_widget.insert(tk.END, f"', Cell ", "bullet_point")
                            self.text_widget.insert(tk.END, f"{finding['cell']}\n", "cell_bold")
                            
                            # Truncate long values
                            display_value = finding['value']
                            if len(display_value) > 200:
                                display_value = display_value[:200] + "..."
                            self.text_widget.insert(tk.END, f"    Value: {display_value}\n\n", "value_text")
                        
                        self.text_widget.insert(tk.END, "-" * 100 + "\n\n", "separator")
                except Exception as e:
                    import logging
                    logging.error(f"Error displaying results for file {file_path}: {e}")
                    self.text_widget.insert(tk.END, f"Error displaying results for {file_path}: {e}\n\n", "error_text_red")
            
            # Add summary at the top with manual spacing
            summary = f"Found {total_matches_count} matches in {files_with_matches} files (out of {len(self.results_map)} processed files that had findings).\n\n\n"  # Extra newline for spacing
            self.text_widget.insert("1.0", summary, "summary_bold")
        except Exception as e:
            import logging
            logging.error(f"Error displaying results: {e}")
            self.text_widget.insert(tk.END, f"Error displaying results: {e}\n", "error_text_red")
