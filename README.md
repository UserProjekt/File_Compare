# File_Compare

A Python command-line tool for comparing files between directories, with special support for video file proxy workflows.

- **Two Comparison Modes:**
  - **Normal Mode**: Compare all files by full filename (basename + extension)
  - **Proxy Mode**: Compare video files by basename only (ignoring extensions)

- **Advanced Proxy Verification**: Optional frame count comparison to detect incomplete proxy files (requires mediainfo CLI)

- **Multiple Directory Support**: Combine multiple directories into single comparison groups using `+` separator

- **Multiple Export Formats**: Export results in JSON, TXT, CSV, or HTML format

- **Smart File Filtering**: Automatically skips system files and directories:
  - macOS: `.DS_Store`, `._*`, `.Trash`, `.AppleDouble`, etc.
  - Windows: `Thumbs.db`, `$RECYCLE.BIN`, `System Volume Information`
  - NAS systems: `@eaDir`, `#recycle`

- **Unicode Support**: Properly handles non-ASCII filenames (Chinese, Japanese, etc.)

- **Parallel Scanning**: Uses multi-threading for faster directory scanning

## Prerequisites

- Python 3.6 or higher
- **Optional**: `mediainfo` CLI tool (required for advanced proxy mode with frame count verification)

### Installing mediainfo (Optional)

**macOS:**
```zsh
brew install mediainfo
```

**Linux:**
```zsh
sudo apt-get install mediainfo
```

**Windows:**
Download from [MediaArea.net](https://mediaarea.net/en/MediaInfo/Download)

## Installation

Clone the Repository

```zsh
git clone https://github.com/yourusername/File_Compare.git
cd File_Compare
```

No additional Python dependencies required - uses Python standard library only.

## Project Structure

```
File_Compare/
├── file_compare.py         # Main entry point
├── src/
│   ├── __init__.py        # Version and package info
│   ├── normal_compare.py  # Normal comparison mode
│   ├── proxy_compare.py   # Proxy comparison mode
│   ├── file_utils.py      # File filtering utilities
│   └── exporters.py       # Export format handlers
└── README.md
```

## Usage

### Basic Syntax

```zsh
python file_compare.py [OPTIONS] PATH1 PATH2
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-f, --format` | Output format: `json`, `txt`, `csv`, `html` | `txt` |
| `-m, --mode` | Comparison mode: `normal`, `proxy` | `normal` |
| `-a, --adv, --advanced` | Advanced mode: compare frame counts (proxy mode only, requires mediainfo) | `False` |
| `-o, --output` | Output filename | `comparison_results_[datetime].[format]` |
| `-h, --help` | Show help message | - |


### Normal Mode (Default)

Compares files by their complete filename including extension.

- **Use case**: General file comparison, backup verification
- **Key**: `filename.extension`
- **Example**: `video.mp4` and `video.mov` are treated as different files

### Proxy Mode

Compares video files by basename only, ignoring file extensions.

- **Use case**: Video proxy workflows where originals and proxies have different formats
- **Key**: `filename` (without extension)
- **Example**: `video.mp4` and `video.mov` are treated as the same file
- **Supported formats**: `.mp4`, `.mov`, `.mxf`, `.avi`, `.mkv`, `.m4v`, `.mpg`, `.mpeg`, `.webm`, `.flv`, `.vob`, `.ogv`, `.ogg`, `.dv`, `.qt`, `.f4v`, `.m2ts`, `.ts`, `.3gp`, `.3g2`

### Advanced Proxy Mode

Adds frame count verification to detect incomplete proxy files.

- **Requirements**: mediainfo CLI tool must be installed
- **Use case**: Verify that proxy files have the same number of frames as originals
- **Detection**: Identifies proxies that may have been cut short during encoding
- **Flag**: `-a`, `--adv`, or `--advanced` (can only be used with `-m proxy`)

## Examples

### Compare Two Single Directories

```zsh
# Normal mode (compare all files)
python file_compare.py /path/to/dir1 /path/to/dir2

# Proxy mode (compare video files by basename)
python file_compare.py -m proxy /path/to/originals /path/to/proxies

# Advanced proxy mode (also verify frame counts)
python file_compare.py -m proxy -a /path/to/originals /path/to/proxies

# Export to HTML
python file_compare.py -f html /path/to/dir1 /path/to/dir2
```

### Compare Multiple Combined Directories

```zsh
# Combine multiple source directories
python file_compare.py "/path/dir1+/path/dir2" "/path/dir3"

# Compare two groups of directories
python file_compare.py "/path/a1+/path/a2+/path/a3" "/path/b1+/path/b2"

# With custom output
python file_compare.py -f html -o results.html "/dir1+/dir2" "/dir3+/dir4"
```

### Real-World Scenarios

**Video Production Workflow:**
```zsh
# Compare original footage with proxy files
python file_compare.py -m proxy -f html \
  /Volumes/Storage/Originals \
  /Volumes/EditDrive/Proxies

# Advanced verification with frame count checking
python file_compare.py -m proxy --advanced -f html \
  /Volumes/Storage/Originals \
  /Volumes/EditDrive/Proxies
```

**Backup Verification:**
```zsh
# Verify backup across multiple drives
python file_compare.py -f csv \
  "/Volumes/Backup1+/Volumes/Backup2" \
  /Volumes/Master
```

**Multi-Location Archive:**
```zsh
# Compare files from multiple archive locations
python file_compare.py -f json \
  "/Archive/2024/Q1+/Archive/2024/Q2+/Archive/2024/Q3" \
  /CurrentProjects
```

**Quality Control for Proxy Encoding:**
```zsh
# Verify all proxies are complete (not truncated)
python file_compare.py -m proxy -a -o proxy_qc.html -f html \
  /Production/Camera_Originals \
  /Production/Proxies
```

## Updates

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



