"""
Test script to verify the improved search responsiveness.
This script will test the improved file search functionality.
"""

import os
import time
import threading
from core.file_search import FileSearch

def test_improved_search():
    """
    Test the improved search functionality with frequent status updates.
    """
    print("Testing improved search responsiveness...")
    print("="*50)
    
    # Create a cancel event
    cancel_event = threading.Event()
    
    # Create file search instance
    file_search = FileSearch(cancel_event)
    
    # Test status callback
    status_updates = []
    last_update_time = time.time()
    
    def status_callback(msg):
        nonlocal last_update_time, status_updates
        current_time = time.time()
        time_since_last = current_time - last_update_time
        status_updates.append((msg, time_since_last))
        print(f"[{time_since_last:.3f}s] {msg}")
        last_update_time = current_time
    
    # Test folders (Desktop and Downloads are common test locations)
    desktop_path = os.path.expanduser("~/Desktop")
    downloads_path = os.path.expanduser("~/Downloads")
    
    test_folders = []
    if os.path.exists(desktop_path):
        test_folders.append(desktop_path)
    if os.path.exists(downloads_path):
        test_folders.append(downloads_path)
    
    if not test_folders:
        print("No test folders found. Using current directory.")
        test_folders = ["."]
    
    print(f"Testing search in: {test_folders}")
    print("Starting search...")
    
    start_time = time.time()
    
    try:
        # Search for Excel files
        results = file_search.search_by_filename(
            test_folders,
            ["test", "data", "excel"],  # Common keywords
            status_callback=status_callback
        )
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print("\n" + "="*50)
        print(f"SEARCH COMPLETED in {total_time:.2f} seconds")
        print(f"Found {len(results)} files")
        print(f"Status updates: {len(status_updates)}")
        
        if status_updates:
            update_intervals = [update[1] for update in status_updates[1:]]  # Skip first
            avg_interval = sum(update_intervals) / len(update_intervals) if update_intervals else 0
            max_interval = max(update_intervals) if update_intervals else 0
            
            print(f"Average update interval: {avg_interval:.3f}s")
            print(f"Maximum update interval: {max_interval:.3f}s")
            print(f"Updates per second: {len(status_updates)/total_time:.1f}")
            
            # Check if we achieved good responsiveness (updates every 0.5s or better)
            if max_interval <= 0.5:
                print("✅ EXCELLENT responsiveness achieved!")
            elif max_interval <= 1.0:
                print("✅ GOOD responsiveness achieved!")
            else:
                print("⚠️  Could be more responsive")
        
        print("\nFirst few results:")
        for i, (filename, filepath, modtime) in enumerate(results[:5]):
            print(f"  {i+1}. {filename}")
            print(f"     Path: {filepath}")
            print(f"     Modified: {modtime}")
            print()
            
    except Exception as e:
        print(f"Error during test: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_improved_search()
    if success:
        print("\n🎉 Test completed successfully!")
        print("The improved search should now be much more responsive.")
    else:
        print("\n❌ Test failed. Please check the error messages above.")
