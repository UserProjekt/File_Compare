import os
from src.file_utils import get_video_extensions, should_skip_file, should_skip_directory, should_skip_path

def get_files_dict(directory):
    """Get dictionary of video files with basename as key and full path as value"""
    files_dict = {}
    video_extensions = get_video_extensions()
    
    for root, dirs, files in os.walk(directory):
        # Skip system directories by modifying dirs in-place
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]
        
        # Skip if current path contains any system directories
        if should_skip_path(root):
            continue
            
        for file in files:
            if should_skip_file(file):
                continue
            
            # Check if it's a video file
            extension = os.path.splitext(file)[1].lower()
            if extension not in video_extensions:
                continue
            
            full_path = os.path.join(root, file)
            # Use basename (without extension) as key for proxy mode
            basename = os.path.splitext(file)[0]
            
            # If basename already exists, keep the first occurrence
            if basename not in files_dict:
                files_dict[basename] = full_path
    
    return files_dict