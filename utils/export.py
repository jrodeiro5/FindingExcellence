"""
Export functionality module.

This module handles exporting search results to various formats.
"""

import os
import csv
import logging

class ExportManager:
    """
    Handles exporting search results to files.
    """
    
    @staticmethod
    def export_filename_results(results, filepath):
        """
        Export filename search results to a CSV file.
        
        Args:
            results: List of filename search results (tuples or treeview items)
            filepath: Path to save the file
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["File Name", "Full Path", "Modified Date"])  # Header
                
                # Handle both raw tuples and treeview items
                if isinstance(results, list) and results and isinstance(results[0], tuple):
                    # Direct list of tuples
                    for row in results:
                        writer.writerow(row)
                else:
                    # Treeview items (ids that need values extracted)
                    for item_id in results:
                        if hasattr(item_id, 'values'):
                            # Direct values property
                            row = item_id.values
                        elif hasattr(results, 'item'):
                            # Treeview with item method
                            row = results.item(item_id, 'values')
                        else:
                            # Assume it's already the values
                            row = item_id
                        writer.writerow(row)
                        
            logging.info(f"Filename results exported to {filepath}")
            return True
        except Exception as e:
            logging.error(f"Error exporting filename results: {e}", exc_info=True)
            return False
    
    @staticmethod
    def export_content_results(results_map, filepath):
        """
        Export content search results to a file (CSV or TXT).
        
        Args:
            results_map: Dictionary mapping file paths to their search results
            filepath: Path to save the file
            
        Returns:
            bool: True if export successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if filepath.endswith('.csv'):
                    # CSV export
                    writer = csv.writer(f)
                    writer.writerow(["File Path", "Keyword", "Sheet", "Cell", "Value Snippet"])
                    
                    for file_path, findings in results_map.items():
                        # Handle error entries
                        if len(findings) == 1 and 'error' in findings[0]:
                            writer.writerow([file_path, "ERROR", "", "", findings[0]['error']])
                            continue
                            
                        # Handle normal findings
                        for finding in findings:
                            # Get a truncated value for CSV
                            value_snippet = finding['value'][:200] if len(finding['value']) > 200 else finding['value']
                            
                            writer.writerow([
                                file_path,
                                finding['keyword'],
                                finding['sheet'],
                                finding['cell'],
                                value_snippet
                            ])
                else:
                    # Text file export (more readable format)
                    for file_path, findings in results_map.items():
                        f.write(f"File: {os.path.basename(file_path)}\n")
                        f.write(f"Path: {file_path}\n\n")
                        
                        # Handle error entries
                        if len(findings) == 1 and 'error' in findings[0]:
                            f.write(f"  ERROR: {findings[0]['error']}\n\n")
                            f.write("-" * 80 + "\n\n")
                            continue
                            
                        # Handle normal findings
                        for finding in findings:
                            f.write(f"  • Keyword '{finding['keyword']}' found in Sheet '{finding['sheet']}', Cell {finding['cell']}\n")
                            
                            # Truncate long values
                            display_value = finding['value']
                            if len(display_value) > 200:
                                display_value = display_value[:200] + "..."
                                
                            f.write(f"    Value: {display_value}\n\n")
                        f.write("-" * 80 + "\n\n")
                        
            logging.info(f"Content results exported to {filepath}")
            return True
        except Exception as e:
            logging.error(f"Error exporting content results: {e}", exc_info=True)
            return False
