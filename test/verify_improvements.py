"""
Quick verification script for the search improvements.
Run with: py verify_improvements.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🔍 Verifying FindingExcellence Search Improvements")
print("=" * 50)

# Check if the improvements are in place
try:
    with open("core/file_search.py", "r") as f:
        content = f.read()
        
    improvements_found = []
    
    # Check for time-based updates
    if "UPDATE_INTERVAL = 0.2" in content:
        improvements_found.append("✅ Time-based updates (200ms)")
    else:
        improvements_found.append("❌ Time-based updates missing")
    
    # Check for frequent directory updates
    if "processed_dirs % 1 == 0" in content:
        improvements_found.append("✅ Frequent directory updates")
    else:
        improvements_found.append("❌ Frequent directory updates missing")
    
    # Check for frequent file updates  
    if "processed_files % 10 == 0" in content:
        improvements_found.append("✅ Frequent file updates (every 10 files)")
    else:
        improvements_found.append("❌ Frequent file updates missing")
    
    # Check for enhanced status messages
    if "os.path.basename(root_dir)" in content:
        improvements_found.append("✅ Enhanced status messages")
    else:
        improvements_found.append("❌ Enhanced status messages missing")
    
    # Check for immediate match feedback
    if "Found {len(found_files)} matching files so far" in content:
        improvements_found.append("✅ Immediate match feedback")
    else:
        improvements_found.append("❌ Immediate match feedback missing")
    
    print("File Search Improvements:")
    for improvement in improvements_found:
        print(f"  {improvement}")
    
    print()
    
    # Check main_window.py improvements
    with open("ui/main_window.py", "r") as f:
        ui_content = f.read()
    
    ui_improvements = []
    
    # Check for enhanced status callback
    if "self.root.after(0, lambda: self.root.update_idletasks())" in ui_content:
        ui_improvements.append("✅ Enhanced UI status callback")
    else:
        ui_improvements.append("❌ Enhanced UI status callback missing")
    
    print("UI Improvements:")
    for improvement in ui_improvements:
        print(f"  {improvement}")
    
    print()
    
    # Check if backup files exist
    backup_files = [
        "core/file_search.py.backup",
        "ui/main_window.py.backup"
    ]
    
    print("Backup Files:")
    for backup in backup_files:
        if os.path.exists(backup):
            print(f"  ✅ {backup}")
        else:
            print(f"  ❌ {backup} missing")
    
    print()
    
    # Overall assessment
    total_checks = len(improvements_found) + len(ui_improvements) + len(backup_files)
    passed_checks = sum(1 for item in improvements_found + ui_improvements if "✅" in item)
    passed_checks += sum(1 for backup in backup_files if os.path.exists(backup))
    
    print(f"Overall Status: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 All improvements successfully implemented!")
        print("\nNext steps:")
        print("1. Run: py main.py")
        print("2. Test search functionality")
        print("3. Build executable when ready")
    else:
        print("⚠️  Some improvements may be missing. Please check the details above.")
        
except Exception as e:
    print(f"❌ Error verifying improvements: {e}")
    print("Please ensure you're running this from the FindingExcellence directory")

print("\n" + "=" * 50)
print("Verification complete!")
