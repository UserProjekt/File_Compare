import os

def should_skip_file(filename):
    """Check if a filename should be skipped"""
    skip_patterns = [
        '._',           # macOS resource fork files
        '.DS_Store',    # macOS folder metadata
        '.AppleDouble', # macOS resource fork directory
        '.Spotlight-V100', # macOS spotlight index
        '.Trashes',     # macOS trash
        '.fseventsd',   # macOS file system events
        'Thumbs.db',    # Windows thumbnail cache
        'desktop.ini'   # Windows folder settings
    ]
    
    return any(filename.startswith(pattern) for pattern in skip_patterns)

def should_skip_directory(dirname):
    """Check if a directory name should be skipped"""
    skip_directories = [
        '$RECYCLE.BIN',  # Windows recycle bin
        'System Volume Information',  # Windows system folder
        '.Trash',        # Linux/macOS trash
        '@eaDir',        # Synology NAS system folder
        '#recycle'       # Some NAS systems recycle folder
    ]
    
    return dirname in skip_directories

def should_skip_path(path):
    """Check if a path contains any directories that should be skipped"""
    skip_directories = [
        '$RECYCLE.BIN',  # Windows recycle bin
        'System Volume Information',  # Windows system folder
        '.Trash',        # Linux/macOS trash
        '@eaDir',        # Synology NAS system folder
        '#recycle'       # Some NAS systems recycle folder
    ]
    
    path_parts = path.split(os.sep)
    return any(part in skip_directories for part in path_parts)

def is_video_file(filename):
    """Check if file is video"""
    video_extensions = {
        '.mp4', '.mov', '.mxf',  # Common video formats
        '.avi', '.wmv', '.mkv',
        '.m4v', '.mpg', '.mpeg',
        '.webm', '.flv', '.vob',
        '.ogv', '.ogg', '.dv',
        '.qt', '.f4v', '.m2ts',
        '.ts', '.3gp', '.3g2'
    }
    return os.path.splitext(filename)[1].lower() in video_extensions

def get_video_extensions():
    """Get set of video extensions"""
    return {
        '.mp4', '.mov', '.mxf',  # Common video formats
        '.avi', '.wmv', '.mkv',
        '.m4v', '.mpg', '.mpeg',
        '.webm', '.flv', '.vob',
        '.ogv', '.ogg', '.dv',
        '.qt', '.f4v', '.m2ts',
        '.ts', '.3gp', '.3g2'
    }