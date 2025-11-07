import os
from src.file_utils import (get_video_extensions, should_skip_file, 
                            should_skip_directory, should_skip_path,
                            get_video_frame_count, check_mediainfo_installed)

def get_files_dict(directory):
    """
    Get dictionary of video files with metadata
    Returns: dict with basename as key and dict of {path, frame_count} as value
    """
    if not check_mediainfo_installed():
        print("\nError: mediainfo CLI is not installed!")
        print("Please install mediainfo:")
        print("  macOS:   brew install mediainfo")
        print("  Windows: Download from https://mediaarea.net/en/MediaInfo/Download")
        print("  Linux:   sudo apt-get install mediainfo")
        import sys
        sys.exit(1)
    
    files_dict = {}
    video_extensions = get_video_extensions()
    
    print("  Reading video metadata (this may take a while)...")
    file_count = 0
    
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
            basename = os.path.splitext(file)[0]
            
            # Get frame count
            frame_count = get_video_frame_count(full_path)
            
            file_count += 1
            if file_count % 10 == 0:
                print(f"    Processed {file_count} videos...")
            
            # If basename already exists, keep the first occurrence
            if basename not in files_dict:
                files_dict[basename] = {
                    'path': full_path,
                    'frame_count': frame_count,
                    'filename': file
                }
    
    print(f"    Total: {file_count} videos processed")
    return files_dict