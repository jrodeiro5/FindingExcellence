"""
Enhanced debug version of FindingExcellence.

This script provides detailed logging of the application startup
to help diagnose initialization issues.
"""

import tkinter as tk
import sys
import os
import traceback
import logging

def setup_logging():
    """Set up basic logging to both file and console."""
    logging.basicConfig(
        filename="debug_output.log",
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Add console handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logging.getLogger('').addHandler(console)
    
    return logging.getLogger('debug')

def check_imports():
    """Test importing all the main modules and report issues."""
    logger = logging.getLogger('debug')
    logger.info("Checking imports...")
    
    # List of modules to check
    modules_to_check = [
        # Core modules
        ('ui.main_window', 'ExcelFinderApp'),
        ('core.config_manager', 'ConfigManager'),
        ('core.file_search', 'FileSearch'),
        ('core.content_search', 'ContentSearch'),
        ('core.excel_processor', 'ExcelProcessor'),
        
        # UI modules
        ('ui.search_panel', 'SearchPanel'),
        ('ui.results_panel', 'ResultsPanel'),
        ('ui.content_search_panel', 'ContentSearchPanel'),
        ('ui.dialogs', 'ContentResultsDialog'),
        
        # Utility modules
        ('utils.logging_setup', 'setup_logging'),
        ('utils.export', 'ExportManager')
    ]
    
    all_successful = True
    
    for module_name, class_name in modules_to_check:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            logger.info(f"✓ Successfully imported {class_name} from {module_name}")
        except ImportError as e:
            logger.error(f"✗ Failed to import module {module_name}: {e}")
            all_successful = False
        except AttributeError as e:
            logger.error(f"✗ Failed to find {class_name} in {module_name}: {e}")
            all_successful = False
        except Exception as e:
            logger.error(f"✗ Unknown error importing {module_name}.{class_name}: {e}")
            all_successful = False
    
    return all_successful

def main():
    """Run a minimal test with detailed diagnostic information."""
    logger = setup_logging()
    logger.info("Starting diagnostic test")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current directory: {os.getcwd()}")
    
    try:
        # Check imports first
        if not check_imports():
            logger.error("Some imports failed. See above for details.")
            return False
        
        # Initialize Tkinter
        logger.info("Initializing Tkinter...")
        root = tk.Tk()
        root.title("FindingExcellence Debug Test")
        root.geometry("400x300")
        
        # Display diagnostic info
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(main_frame, text="Diagnostic Test", font=("Helvetica", 16, "bold")).pack(pady=10)
        tk.Label(main_frame, text="If you can see this window, Tkinter is working correctly!").pack(pady=10)
        tk.Label(main_frame, text=f"Python version: {sys.version}").pack(anchor="w")
        tk.Label(main_frame, text=f"Tkinter version: {tk.TkVersion}").pack(anchor="w")
        
        # Now try to import and initialize the main application components
        try:
            from ui.main_window import ExcelFinderApp
            from core.config_manager import ConfigManager
            
            # Create a status label to show progress
            status = tk.StringVar(value="Testing imports...")
            status_label = tk.Label(main_frame, textvariable=status, fg="blue")
            status_label.pack(pady=10, fill=tk.X)
            
            # Update status
            def update_status(msg):
                status.set(msg)
                root.update_idletasks()
            
            # Add a button to force check of full application
            def test_full_app():
                try:
                    update_status("Creating config manager...")
                    config = ConfigManager()
                    
                    update_status("Creating application instance...")
                    # Don't actually create it, but import all the necessary modules
                    from core.file_search import FileSearch
                    from core.content_search import ContentSearch
                    from ui.search_panel import SearchPanel
                    from ui.results_panel import ResultsPanel
                    from ui.content_search_panel import ContentSearchPanel
                    
                    update_status("All components imported successfully!")
                    logger.info("All application components imported without errors.")
                    result_label.config(text="All tests passed!\nThe application should start correctly.", fg="green")
                except Exception as e:
                    error_msg = f"Error initializing components: {e}"
                    logger.error(error_msg)
                    logger.error(traceback.format_exc())
                    update_status("Error during initialization!")
                    result_label.config(text=f"Test failed: {str(e)}", fg="red")
            
            # Add button to test initialization
            test_button = tk.Button(main_frame, text="Test Full Application", command=test_full_app)
            test_button.pack(pady=10)
            
            # Result label
            result_label = tk.Label(main_frame, text="Click the button to test initialization", fg="blue")
            result_label.pack(pady=10)
            
        except Exception as e:
            error_msg = f"Failed to import main components: {e}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            tk.Label(main_frame, text=error_msg, fg="red", wraplength=350).pack(pady=10)
        
        # Add close button
        tk.Button(main_frame, text="Close", command=root.destroy).pack(pady=10)
        
        logger.info("Main window created successfully")
        root.mainloop()
        logger.info("Window closed")
        return True
        
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\nDiagnostic test completed successfully.")
        else:
            print("\nDiagnostic test encountered errors. Check debug_output.log for details.")
    except Exception as e:
        print(f"\nFatal error during diagnostic test: {e}")
        traceback.print_exc()
    
    print("\nPress Enter to close...")
    input()
