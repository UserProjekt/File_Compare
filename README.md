# File_Compare

A Python command-line tool for comparing files between directories, with special support for video file proxy workflows.

## Features

- **Two Comparison Modes:**
  - **Normal Mode**: Compare all files by full filename (basename + extension)
  - **Proxy Mode**: Compare video files by basename only (ignoring extensions)

- **Multiple Directory Support**: Combine multiple directories into single comparison groups using `+` separator

- **Multiple Export Formats**: Export results in JSON, TXT, CSV, or HTML format

- **Smart File Filtering**: Automatically skips system files and directories:
  - macOS: `.DS_Store`, `._*`, `.Trash`, `.AppleDouble`, etc.
  - Windows: `Thumbs.db`, `$RECYCLE.BIN`, `System Volume Information`
  - NAS systems: `@eaDir`, `#recycle`

- **Unicode Support**: Properly handles non-ASCII filenames (Chinese, Japanese, etc.)

- **Parallel Scanning**: Uses multi-threading for faster directory scanning

## Installation

### Prerequisites

- Python 3.6 or higher

### Clone the Repository

```zsh
git clone https://github.com/yourusername/file-comparison-tool.git
cd file-comparison-tool
```

No additional dependencies required - uses Python standard library only.

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
| `-o, --output` | Output filename | `comparison_results_[datetime].[format]` |
| `-h, --help` | Show help message | - |

### Examples

#### Compare Two Single Directories

```zsh
# Normal mode (compare all files)
python file_compare.py /path/to/dir1 /path/to/dir2

# Proxy mode (compare video files by basename)
python file_compare.py -m proxy /path/to/originals /path/to/proxies

# Export to HTML
python file_compare.py -f html /path/to/dir1 /path/to/dir2
```

#### Compare Multiple Combined Directories

```zsh
# Combine multiple source directories
python file_compare.py "/path/dir1+/path/dir2" "/path/dir3"

# Compare two groups of directories
python file_compare.py "/path/a1+/path/a2+/path/a3" "/path/b1+/path/b2"

# With custom output
python file_compare.py -f html -o results.html "/dir1+/dir2" "/dir3+/dir4"
```

#### Real-World Scenarios

**Video Production Workflow:**
```zsh
# Compare original footage with proxy files
python file_compare.py -m proxy -f html \
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

## Comparison Modes

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

## Output Formats



## Project Structure

```
file-comparison-tool/
├── file_compare.py         # Main entry point
├── src/
│   ├── __init__.py        # Version and package info
│   ├── normal_compare.py  # Normal comparison mode
│   ├── proxy_compare.py   # Proxy comparison mode
│   ├── file_utils.py      # File filtering utilities
│   └── exporters.py       # Export format handlers
└── README.md
```

## Version History

### v1.1.3 (Current)
- Fixed system directory skipping ($RECYCLE.BIN, .Trash, etc.)
- Improved directory traversal to skip system folders entirely

### v1.1.2
- Added display of absolute output file path

### v1.1.1
- Fixed character encoding issues for non-ASCII filenames
- Improved HTML output for Safari compatibility
- Added UTF-8 BOM for better browser/Excel support

### v1.1.0
- Added multiple directory comparison support with `+` separator
- Parallel directory scanning for improved performance

### v1.0.0
- Initial release with normal and proxy comparison modes
- Support for JSON, TXT, CSV, HTML export formats
