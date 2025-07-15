"""
Content search module.

This module contains functionality for searching content within Excel files.
"""

import os
import logging
import threading
import concurrent.futures
from core.excel_processor import ExcelProcessor

class ContentSearch:
    """
    Handles content-based searching within files.
    """
    
    def __init__(self, cancel_event=None, max_workers=None):
        """
        Initialize the content search functionality.
        
        Args:
            cancel_event: Threading event for cancellation
            max_workers: Maximum number of worker threads
        """
        self.cancel_event = cancel_event or threading.Event()
        
        if max_workers is None:
            # Using fewer workers by default to avoid overwhelming systems
            max_workers = max(1, os.cpu_count() // 2)
            
        # Initialize ThreadPoolExecutor for content search
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    
    def search_files_contents(self, files_to_search, keywords, case_sensitive=False,
                             progress_callback=None):
        """
        Search for keywords within the content of multiple files.
        
        Args:
            files_to_search: List of file paths to search
            keywords: List of keywords to find
            case_sensitive: Whether to perform case-sensitive search
            progress_callback: Function to call with progress updates
            
        Returns:
            dict: Dictionary mapping file paths to their search results
        """
        all_results_map = {}  # Map path to results list
        processed_count = 0
        
        try:
            # Submit all search tasks to the executor
            futures = [
                self.executor.submit(self._process_single_file, file_path, keywords, case_sensitive)
                for file_path in files_to_search
            ]
            
            # Process completed futures as they finish
            for future in concurrent.futures.as_completed(futures):
                if self.cancel_event.is_set():
                    # Attempt to cancel pending futures (works only in Python 3.9+)
                    for f in futures:
                        if not f.done(): 
                            f.cancel()
                    logging.info("Content search cancelled during future processing.")
                    break
                    
                try:
                    file_path, single_file_results = future.result()
                    if single_file_results:  # Only add if there are findings or errors
                        all_results_map[file_path] = single_file_results
                except concurrent.futures.CancelledError:
                    logging.info("A content search task was cancelled.")
                except Exception as e:
                    # Handle unhandled errors from futures
                    logging.error(f"Unhandled error from content search future: {e}", exc_info=True)
                finally:
                    processed_count += 1
                    if progress_callback:
                        progress_callback(processed_count, len(files_to_search))
        
        except Exception as e:
            logging.error(f"Error in content search executor: {e}", exc_info=True)
            raise
            
        return all_results_map
    
    def _process_single_file(self, file_path, keywords, case_sensitive):
        """
        Process a single file for content searching.
        
        Args:
            file_path: Path to the file
            keywords: List of keywords to search for
            case_sensitive: Whether to use case-sensitive search
            
        Returns:
            tuple: (file_path, results_list)
        """
        if self.cancel_event.is_set():
            return file_path, []  # Return empty if cancelled
            
        # Use the ExcelProcessor to handle the Excel file
        results = ExcelProcessor.search_content(file_path, keywords, case_sensitive)
        
        return file_path, results
    
    def cancel(self):
        """
        Cancel an ongoing search.
        """
        self.cancel_event.set()
    
    def shutdown(self):
        """
        Properly shut down the executor and clean up resources.
        """
        # cancel_futures is Python 3.9+
        has_cancel_futures = hasattr(concurrent.futures, 'CancelledError')
        self.executor.shutdown(wait=True, cancel_futures=has_cancel_futures)
