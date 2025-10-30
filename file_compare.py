import argparse
import sys
import time
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from src import normal_compare, proxy_compare
from src.exporters import Exporter

def parse_directory_groups(path_str):
    """Parse directory groups like 'dir1+dir2+dir3' into list of paths"""
    paths = [p.strip() for p in path_str.split('+')]
    
    # Validate all paths exist
    for path in paths:
        if not os.path.exists(path):
            print(f"Error: Path does not exist: {path}")
            sys.exit(1)
    
    return paths

def merge_files_dicts(files_dicts, mode='normal'):
    """Merge multiple file dictionaries, handling conflicts"""
    merged = {}
    conflicts = []
    
    for files_dict in files_dicts:
        for key, path in files_dict.items():
            if key in merged:
                # Handle conflict - keep first occurrence but log it
                conflicts.append({
                    'key': key,
                    'existing_path': merged[key],
                    'new_path': path
                })
            else:
                merged[key] = path
    
    return merged, conflicts

def scan_multiple_directories(directories, compare_module):
    """Scan multiple directories in parallel and merge results"""
    all_files_dicts = []
    
    with ThreadPoolExecutor(max_workers=min(len(directories), 4)) as executor:
        future_to_dir = {executor.submit(compare_module.get_files_dict, dir_path): dir_path 
                        for dir_path in directories}
        
        for future in as_completed(future_to_dir):
            dir_path = future_to_dir[future]
            try:
                files_dict = future.result()
                all_files_dicts.append(files_dict)
                print(f"  Scanned {dir_path}: {len(files_dict)} files")
            except Exception as e:
                print(f"  Error scanning {dir_path}: {str(e)}")
    
    # Merge all dictionaries
    merged_dict, conflicts = merge_files_dicts(all_files_dicts)
    
    if conflicts:
        print(f"  Warning: {len(conflicts)} filename conflicts found (kept first occurrence)")
    
    return merged_dict

def main():
    parser = argparse.ArgumentParser(
        description='Compare files between directories',
        epilog='Examples:\n'
               '  Single directories: python file_compare.py /path/a /path/b\n'
               '  Multiple directories: python file_compare.py "/path/a1+/path/a2" "/path/b1+/path/b2"',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('path1', help='First directory path(s), use + to combine multiple dirs (e.g., "dir1+dir2")')
    parser.add_argument('path2', help='Second directory path(s), use + to combine multiple dirs (e.g., "dir1+dir2")')
    parser.add_argument('-f', '--format', choices=['json', 'txt', 'csv', 'html'], 
                        default='txt', help='default: txt')
    parser.add_argument('-m', '--mode', 
                        choices=['normal', 'proxy'],
                        default='normal', 
                        help='normal: compare all files by basename.extension | '
                             'proxy: compare video files by basename only')
    parser.add_argument('-o', '--output', help='Output file name (default: comparison_results_[datetime].[format])')
    args = parser.parse_args()

    try:
        # Parse directory groups
        dirs1 = parse_directory_groups(args.path1)
        dirs2 = parse_directory_groups(args.path2)
        
        # Set default output filename if not provided
        if not args.output:
            args.output = f"comparison_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{args.format}"
        
        # Convert output path to absolute path
        output_path = os.path.abspath(args.output)

        start_time = time.time()
        
        # Choose mode
        compare_module = normal_compare if args.mode == 'normal' else proxy_compare
        
        print(f"Scanning directories in {args.mode} mode...")
        
        # Scan directory groups
        print(f"Group 1 ({len(dirs1)} directories):")
        files1 = scan_multiple_directories(dirs1, compare_module)
        
        print(f"Group 2 ({len(dirs2)} directories):")
        files2 = scan_multiple_directories(dirs2, compare_module)
        
        print(f"\nTotal found: {len(files1)} unique files in group 1, {len(files2)} unique files in group 2")

        # Compare files
        unique1 = set(files1.keys()) - set(files2.keys())
        unique2 = set(files2.keys()) - set(files1.keys())

        # Export results with updated path information
        print("Exporting results...")
        export_method = getattr(Exporter, f'to_{args.format}')
        
        # Create display paths for multiple directories
        display_path1 = ' + '.join(dirs1) if len(dirs1) > 1 else dirs1[0]
        display_path2 = ' + '.join(dirs2) if len(dirs2) > 1 else dirs2[0]
        
        export_method({
            'mode': args.mode,
            'path1': display_path1,
            'path2': display_path2,
            'dirs1': dirs1,  # Add individual directory lists
            'dirs2': dirs2,
            'unique1': [files1[f] for f in unique1],
            'unique2': [files2[f] for f in unique2]
        }, output_path)

        print(f"\nResults have been exported to: {output_path}")
        print(f"Files only in group 1: {len(unique1)}")
        print(f"Files only in group 2: {len(unique2)}")
        print(f"Total execution time: {time.time() - start_time:.2f} seconds")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()