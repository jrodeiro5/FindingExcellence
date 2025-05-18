"""
File search module.

This module contains functionality for searching files by filename criteria.
"""

import os
import datetime
import logging
import threading
from core.excel_processor import ExcelProcessor

class FileSearch:
    """
    Handles filename-based searching.
    """
    
    def __init__(self, cancel_event=None):
        """
        Initialize the file search functionality.
        
        Args:
            cancel_event: Threading event for cancellation
        """
        self.cancel_event = cancel_event or threading.Event()
    
    def search_by_filename(self, folder_paths, filename_keywords, 
                          start_date=None, end_date=None, 
                          exclude_keywords=None, case_sensitive=False,
                          supported_extensions=None, 
                          status_callback=None):
        """
        Search for files matching given criteria.
        
        Args:
            folder_path: Root folder to search in
            filename_keywords: List of keywords to find in filenames
            start_date: Earliest modified date to include
            end_date: Latest modified date to include
            exclude_keywords: Keywords to exclude from results
            case_sensitive: Whether to perform case-sensitive search
            supported_extensions: List of file extensions to include
            status_callback: Function to call with status updates
            
        Returns:
            list: List of matching files with metadata (name, path, modified_date)
        """
        if supported_extensions is None:
            supported_extensions = ExcelProcessor.SUPPORTED_EXTENSIONS
            
        if exclude_keywords is None:
            exclude_keywords = []
            
        # Convert folder_paths to list if a string was provided
        if isinstance(folder_paths, str):
            folder_paths = [folder_paths]
            
        # Log the folder paths to help with debugging
        logging.info(f"Searching in folder paths: {folder_paths}")
            
        found_files = []
        processed_dirs = 0
        processed_files = 0
        
        try:
            # Iterate through each provided folder
            for folder_path in folder_paths:
                if not os.path.isdir(folder_path):
                    logging.warning(f"Skipping non-existent folder: {folder_path}")
                    continue
                    
                if status_callback:
                    status_callback(f"Searching in folder: {folder_path}...")
                
                for root_dir, dirs, files in os.walk(folder_path):
                    processed_dirs += 1
                
                    # Update status every 10 directories
                    if processed_dirs % 10 == 0 and status_callback:
                        status_callback(f"Scanning: Directory {processed_dirs}, {processed_files} files processed...")
                    
                    if self.cancel_event.is_set():
                        logging.info("Filename search cancelled during directory walk.")
                        break  # Break from inner loop
                
                    # Filter out excluded directories based on case sensitivity
                    if not case_sensitive:
                        dirs[:] = [d for d in dirs if not any(ex.lower() in d.lower() for ex in exclude_keywords)]
                    else:
                        dirs[:] = [d for d in dirs if not any(ex in d for ex in exclude_keywords)]

                    for file in files:
                        processed_files += 1
                        
                        # Update status every 100 files
                        if processed_files % 100 == 0 and status_callback:
                            status_callback(f"Scanning: {processed_files} files processed...")
                        
                        if self.cancel_event.is_set():
                            logging.info("Filename search cancelled during file walk.")
                            break  # Break from inner loop

                        file_lower = file.lower()
                        if not file_lower.endswith(supported_extensions):
                            continue
                        
                        filename_to_check = file if case_sensitive else file_lower
                        
                        # Check if filename contains any of the keywords
                        if filename_keywords:
                            match_found = False
                            for kw in filename_keywords:
                                kw_to_check = kw if case_sensitive else kw.lower()
                                if kw_to_check in filename_to_check:
                                    match_found = True
                                    break
                            if not match_found:
                                continue
                    
                        file_path = os.path.join(root_dir, file)
                        
                        # Check date range if specified
                        if start_date or end_date:
                            try:
                                mod_timestamp = os.path.getmtime(file_path)
                                mod_date = datetime.date.fromtimestamp(mod_timestamp)
                                if start_date and mod_date < start_date: continue
                                if end_date and mod_date > end_date: continue
                            except OSError as e:  # File might have been moved/deleted
                                logging.warning(f"Could not getmtime for {file_path}: {e}")
                                continue
                        
                        # Get formatted modified time
                        mod_time_dt = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                        formatted_time = mod_time_dt.strftime('%Y-%m-%d %H:%M:%S')
                        
                        # Add to results
                        found_files.append((file, file_path, formatted_time))
                
                    # Check for cancellation after processing a directory
                    if self.cancel_event.is_set(): 
                        break  # Break from inner directory walk loop
                        
                # Check for cancellation after processing a folder
                if self.cancel_event.is_set():
                    break  # Break from outer folder loop
                    
        except Exception as e:
            logging.error(f"Error during filename search: {e}", exc_info=True)
            raise
            
        return found_files
    
    def cancel(self):
        """
        Cancel an ongoing search.
        """
        self.cancel_event.set()
