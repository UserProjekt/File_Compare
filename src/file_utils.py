import os
import subprocess
import json

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

def check_mediainfo_installed():
    """Check if mediainfo CLI is installed"""
    try:
        subprocess.run(['mediainfo', '--Version'], 
                      capture_output=True, 
                      check=True,
                      timeout=5)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return False

def get_video_frame_count(video_path):
    """
    Get frame count of video file using mediainfo CLI
    Returns None if unable to get frame count
    """
    try:
        # Run mediainfo with JSON output
        result = subprocess.run(
            ['mediainfo', '--Output=JSON', video_path],
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )
        
        # Parse JSON output
        data = json.loads(result.stdout)
        
        # Navigate the JSON structure to find frame count
        if 'media' in data and 'track' in data['media']:
            for track in data['media']['track']:
                if track.get('@type') == 'Video':
                    # Try different possible fields for frame count
                    frame_count = track.get('FrameCount')
                    if frame_count:
                        return int(frame_count)
                    
                    # Alternative: calculate from duration and frame rate
                    duration = track.get('Duration')
                    frame_rate = track.get('FrameRate')
                    if duration and frame_rate:
                        try:
                            return int(float(duration) * float(frame_rate))
                        except (ValueError, TypeError):
                            pass
        
        return None
        
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, 
            json.JSONDecodeError, FileNotFoundError, ValueError) as e:
        print(f"  Warning: Could not get frame count for {os.path.basename(video_path)}: {str(e)}")
        return None

def get_video_metadata(video_path):
    """
    Get video metadata including frame count, duration, and codec
    Returns dict with metadata or None if failed
    """
    try:
        result = subprocess.run(
            ['mediainfo', '--Output=JSON', video_path],
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )
        
        data = json.loads(result.stdout)
        metadata = {
            'frame_count': None,
            'duration': None,
            'frame_rate': None,
            'codec': None,
            'width': None,
            'height': None
        }
        
        if 'media' in data and 'track' in data['media']:
            for track in data['media']['track']:
                if track.get('@type') == 'Video':
                    metadata['frame_count'] = track.get('FrameCount')
                    metadata['duration'] = track.get('Duration')
                    metadata['frame_rate'] = track.get('FrameRate')
                    metadata['codec'] = track.get('Format')
                    metadata['width'] = track.get('Width')
                    metadata['height'] = track.get('Height')
                    
                    # Calculate frame count if not directly available
                    if not metadata['frame_count'] and metadata['duration'] and metadata['frame_rate']:
                        try:
                            metadata['frame_count'] = int(float(metadata['duration']) * float(metadata['frame_rate']))
                        except (ValueError, TypeError):
                            pass
                    
                    # Convert frame_count to int if it's a string
                    if metadata['frame_count']:
                        try:
                            metadata['frame_count'] = int(metadata['frame_count'])
                        except (ValueError, TypeError):
                            metadata['frame_count'] = None
                    
                    break
        
        return metadata
        
    except Exception as e:
        print(f"  Warning: Could not get metadata for {os.path.basename(video_path)}: {str(e)}")
        return None