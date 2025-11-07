"""
File Comparison Tool
-------------------
A tool for comparing video files between directories.

Usage:
    file_compare.py [-h] [-f {json,txt,csv,html}] [-m {normal,proxy}] [--adv]

Options:
  -h, --help            show this help message and exit
  -f {json,txt,csv,html}, --format {json,txt,csv,html}
                        default: txt
  -m {normal,proxy}, --mode {normal,proxy}
                        normal: compare all files by basename.extension |
                        proxy: compare video files by basename only
  -a --adv --advanced   Advanced mode (proxy only): also compare frame counts
                        to detect incomplete proxy files (requires mediainfo CLI)
  -o OUTPUT, --output OUTPUT
                        Output file name (default:
                        comparison_results_[datetime].[format])







New in v1.1.0:
    Multiple directory comparison support
    - python file_compare.py "/dir1+/dir2" "/dir3"
    - python file_compare.py "/dir1+/dir2+/dir3" "/dir4+/dir5"
    - Use '+' to combine multiple directories into a single comparison group.

New in v1.1.1:
    Fixed character encoding issues for non-ASCII filenames
    - HTML output now properly displays Chinese/Unicode characters in Safari
    - Added UTF-8 BOM to HTML files for better browser compatibility
    - Improved CSV encoding for Excel compatibility

New in v1.1.2:
    Displays the absolute path of output file

New in v1.1.3:
    Fixed system directory skipping ($RECYCLE.BIN, .Trash, etc.)
    - Properly excludes files in Windows Recycle Bin and other system directories
    - Improved directory traversal to skip system folders entirely

New in v1.2.0:
    Advanced proxy comparison mode
    - Use --adv flag with proxy mode to compare frame counts
    - Detects incomplete or corrupted proxy files
    - Reports frame count mismatches between original and proxy files
    - Requires mediainfo CLI tool to be installed
"""

__version__ = '1.2.0'
__author__ = 'userprojekt'