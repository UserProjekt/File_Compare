import os
from src.file_utils import should_skip_file, should_skip_directory, should_skip_path

def get_files_dict(directory):
    """Get dictionary of files with full filename as key and full path as value"""
    files_dict = {}
    
    for root, dirs, files in os.walk(directory):
        # Skip system directories by modifying dirs in-place
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]
        
        # Skip if current path contains any system directories
        if should_skip_path(root):
            continue
            
        for file in files:
            if should_skip_file(file):
                continue
            
            full_path = os.path.join(root, file)
            # Use full filename (with extension) as key
            files_dict[file] = full_path
    
    return files_dict