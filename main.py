"""
Main entry point for the FindingExcellence application.

This script initializes the application, sets up logging,
and launches the main user interface.
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import traceback

from ui.main_window import ExcelFinderApp
from utils.logging_setup import setup_logging

# Global constants
APP_NAME = "FindingExcellence"
VERSION = "1.0.0"

def main():
    """
    Initialize and run the FindingExcellence application.
    """
    # Setup logging
    logger = setup_logging()
    logger.info(f"Starting {APP_NAME} v{VERSION}")
    
    # Print environment info for debugging
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Tkinter version: {tk.TkVersion}")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    try:
        # Initialize Tkinter
        logger.info("Initializing Tkinter...")
        root = tk.Tk()
        root.title(f"{APP_NAME} v{VERSION}")
        
        # Set basic window size
        root.geometry("950x700")
        
        # Try to ensure the window is visible on screen
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f"{width}x{height}+{x}+{y}")
        
        try:
            # Initialize the application
            logger.info("Creating application instance...")
            app = ExcelFinderApp(root)
            
            # Start the main loop
            logger.info("Starting main event loop...")
            root.mainloop()
        except Exception as e:
            error_msg = f"Application initialization failed: {e}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            messagebox.showerror(
                "Application Error",
                f"{error_msg}\n\nPlease check the log file: {os.path.abspath('finding_excellence.log')}"
            )
            raise
            
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        logger.error(traceback.format_exc())
        messagebox.showerror(
            "Fatal Error",
            f"A fatal error occurred: {e}\n\nPlease check the log file for details."
        )
        raise
    
    finally:
        logger.info(f"{APP_NAME} shutting down.")

if __name__ == "__main__":
    main()
