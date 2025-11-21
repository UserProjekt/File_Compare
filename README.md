# File_Compare

A Python command-line tool for comparing files between directories, with special support for video file proxy workflows.

- **Three Comparison Modes:**
  - **Normal Mode**: Compare all files by full filename (basename + extension)
  - **Proxy Mode**: Compare video files by basename only (ignoring extensions)
  - **ProxyAdv Mode**: Proxy mode with frame count verification to detect incomplete proxy files (requires mediainfo CLI)

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
- **Optional**: `mediainfo` CLI tool (required for proxyadv mode with frame count verification)

### Installing mediainfo (Optional - Required for proxyadv mode)

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

## Project Structure

```
File_Compare/
├── file_compare.py              # Main entry point
├── src/
│   ├── __init__.py             # Version and package info
│   ├── normal_compare.py       # Normal comparison mode
│   ├── proxy_compare.py        # Proxy comparison mode
│   ├── proxy_compare_advanced.py # Advanced proxy comparison mode
│   ├── file_utils.py           # File filtering utilities
│   └── exporters.py            # Export format handlers
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
| `-f, --format` | Output format(s): `json`, `txt`, `csv`, `html` (multiple allowed) | `html` |
| `-m, --mode` | Comparison mode: `normal`, `proxy`, `proxyadv` | `normal` |
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

### ProxyAdv Mode

Proxy comparison with frame count verification to detect incomplete proxy files.

- **Requirements**: mediainfo CLI tool must be installed
- **Use case**: Verify that proxy files have the same number of frames as originals

## Examples

### Compare Two Single Directories

```zsh
# Normal mode (compare all files)
python file_compare.py /path/to/dir1 /path/to/dir2

# Proxy mode (compare video files by basename)
python file_compare.py -m proxy /path/to/originals /path/to/proxies

# Advanced proxy mode (verify frame counts)
python file_compare.py -m proxyadv /path/to/originals /path/to/proxies

# Export to HTML and JSON
python file_compare.py -f html json /path/to/dir1 /path/to/dir2
```

### Compare Multiple Combined Directories

```zsh
# Combine multiple source directories
python file_compare.py "/path/dir1+/path/dir2" "/path/dir3"

# Compare two groups of directories
python file_compare.py "/path/a1+/path/a2+/path/a3" "/path/b1+/path/b2"

# With multiple output formats
python file_compare.py -f html json "/dir1+/dir2" "/dir3+/dir4"
```

### Real-World Scenarios

**Video Production Workflow:**
```zsh
# Compare original footage with proxy files
python file_compare.py -m proxy -f html \
  /Volumes/Storage/Originals \
  /Volumes/EditDrive/Proxies

# Compare original footage with proxy files and export to HTML and JSON
python file_compare.py -m proxy -f html json \
  /Volumes/Storage/Originals \
  /Volumes/EditDrive/Proxies

# Advanced verification with frame count checking
python file_compare.py -m proxyadv -f html \
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
python file_compare.py -m proxyadv -f html \
  /Production/Camera_Originals \
  /Production/Proxies
```
