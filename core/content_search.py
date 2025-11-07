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
            
        self.max_workers = max_workers
        # Don't create executor in __init__ to avoid resource leaks
        self.executor = None
        self._current_futures = []
    
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
        
        # Create executor for this search session
        if self.executor is None:
            self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)
        
        try:
            # Submit all search tasks to the executor
            futures = [
                self.executor.submit(self._process_single_file, file_path, keywords, case_sensitive)
                for file_path in files_to_search
            ]
            
            # Store futures for potential cancellation
            self._current_futures = futures
            
            # Process completed futures as they finish
            for future in concurrent.futures.as_completed(futures, timeout=1):
                if self.cancel_event.is_set():
                    logging.info("Content search cancelled - stopping processing.")
                    break
                    
                try:
                    file_path, single_file_results = future.result(timeout=0.1)
                    if single_file_results:  # Only add if there are findings or errors
                        all_results_map[file_path] = single_file_results
                except concurrent.futures.TimeoutError:
                    # Skip this future and continue
                    continue
                except concurrent.futures.CancelledError:
                    logging.info("A content search task was cancelled.")
                except Exception as e:
                    # Handle unhandled errors from futures
                    logging.error(f"Unhandled error from content search future: {e}", exc_info=True)
                finally:
                    processed_count += 1
                    if progress_callback:
                        progress_callback(processed_count, len(files_to_search))
        
        except concurrent.futures.TimeoutError:
            # Normal timeout, check if cancelled
            if self.cancel_event.is_set():
                logging.info("Content search timed out and cancelled.")
        except Exception as e:
            logging.error(f"Error in content search executor: {e}", exc_info=True)
            raise
        finally:
            # Clean up futures list
            self._current_futures = []
            
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
        # Check cancellation before processing
        if self.cancel_event.is_set():
            logging.debug(f"Skipping file {file_path} due to cancellation.")
            return file_path, []
            
        try:
            # Use the ExcelProcessor to handle the Excel file
            # Pass the cancel_event so Excel processor can also check for cancellation
            results = ExcelProcessor.search_content(file_path, keywords, case_sensitive, self.cancel_event)
        except Exception as e:
            # If processing fails, log error and return empty results
            logging.error(f"Error processing file {file_path}: {e}")
            results = [{'error': f"Error processing file: {str(e)}", 'file_path': file_path}]
        
        return file_path, results
    
    def cancel(self):
        """
        Cancel an ongoing search.
        """
        self.cancel_event.set()
        
        # Cancel all current futures if possible
        for future in self._current_futures:
            if not future.done():
                future.cancel()
        
        logging.info("Content search cancellation requested and futures cancelled.")
    
    def shutdown(self):
        """
        Properly shut down the executor and clean up resources.
        """
        if self.executor is not None:
            # First cancel any running futures
            for future in self._current_futures:
                if not future.done():
                    future.cancel()
            
            # Try to shut down gracefully with cancel_futures if available (Python 3.9+)
            try:
                # Check if cancel_futures parameter is supported
                import inspect
                sig = inspect.signature(self.executor.shutdown)
                if 'cancel_futures' in sig.parameters:
                    self.executor.shutdown(wait=False, cancel_futures=True)
                else:
                    self.executor.shutdown(wait=False)
            except Exception as e:
                logging.warning(f"Error during executor shutdown: {e}")
                # Force shutdown
                try:
                    self.executor.shutdown(wait=False)
                except:
                    pass
            
            # Clear the executor reference
            self.executor = None
        
        # Clear futures list
        self._current_futures = []
        logging.info("Content search executor shut down successfully.")
