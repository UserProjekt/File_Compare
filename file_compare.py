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

def merge_files_dicts(files_dicts, mode='normal', advanced=False):
    """Merge multiple file dictionaries, handling conflicts"""
    merged = {}
    conflicts = []
    
    for files_dict in files_dicts:
        for key, value in files_dict.items():
            if key in merged:
                # Handle conflict - keep first occurrence but log it
                existing_path = merged[key]['path'] if advanced else merged[key]
                new_path = value['path'] if advanced else value
                conflicts.append({
                    'key': key,
                    'existing_path': existing_path,
                    'new_path': new_path
                })
            else:
                merged[key] = value
    
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

def compare_advanced(files1, files2):
    """
    Advanced comparison for proxy mode with frame count checking
    Returns: unique1, unique2, frame_mismatches
    """
    keys1 = set(files1.keys())
    keys2 = set(files2.keys())
    
    unique1 = keys1 - keys2
    unique2 = keys2 - keys1
    common = keys1 & keys2
    
    # Check frame count mismatches for common files
    frame_mismatches = []
    for basename in common:
        fc1 = files1[basename]['frame_count']
        fc2 = files2[basename]['frame_count']
        
        # Only report mismatch if both have valid frame counts and they differ
        if fc1 is not None and fc2 is not None and fc1 != fc2:
            frame_mismatches.append({
                'basename': basename,
                'file1': files1[basename]['filename'],
                'file2': files2[basename]['filename'],
                'path1': files1[basename]['path'],
                'path2': files2[basename]['path'],
                'frames1': fc1,
                'frames2': fc2,
                'difference': abs(fc1 - fc2)
            })
    
    return unique1, unique2, frame_mismatches

def main():
    parser = argparse.ArgumentParser(
        description='Compare files between directories',
        epilog='Examples:\n'
               '  Single directories: python file_compare.py /path/a /path/b\n'
               '  Multiple directories: python file_compare.py "/path/a1+/path/a2" "/path/b1+/path/b2"\n'
               '  Advanced proxy mode: python file_compare.py -m proxy -a /originals /proxies',
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
    parser.add_argument('-a', '--adv', '--advanced', action='store_true',
                        help='Advanced mode (proxy only): compare frame counts to detect incomplete proxies (requires mediainfo)')
    parser.add_argument('-o', '--output', help='Output file name (default: comparison_results_[datetime].[format])')
    args = parser.parse_args()

    try:
        # Validate advanced mode
        if args.adv and args.mode != 'proxy':
            print("Error: -a/--adv/--advanced flag can only be used with -m proxy mode")
            sys.exit(1)
        
        # Parse directory groups
        dirs1 = parse_directory_groups(args.path1)
        dirs2 = parse_directory_groups(args.path2)
        
        # Set default output filename if not provided
        if not args.output:
            mode_suffix = '_advanced' if args.adv else ''
            args.output = f"comparison_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}{mode_suffix}.{args.format}"
        
        # Convert output path to absolute path
        output_path = os.path.abspath(args.output)

        start_time = time.time()
        
        # Choose mode
        if args.adv:
            from src import proxy_compare_advanced
            compare_module = proxy_compare_advanced
            mode_display = "proxy (advanced)"
        else:
            compare_module = normal_compare if args.mode == 'normal' else proxy_compare
            mode_display = args.mode
        
        print(f"Scanning directories in {mode_display} mode...")
        
        # Scan directory groups
        print(f"Group 1 ({len(dirs1)} directories):")
        files1 = scan_multiple_directories(dirs1, compare_module)
        
        print(f"Group 2 ({len(dirs2)} directories):")
        files2 = scan_multiple_directories(dirs2, compare_module)
        
        print(f"\nTotal found: {len(files1)} unique files in group 1, {len(files2)} unique files in group 2")

        # Compare files
        if args.adv:
            unique1, unique2, frame_mismatches = compare_advanced(files1, files2)
            print(f"Frame count mismatches found: {len(frame_mismatches)}")
        else:
            unique1 = set(files1.keys()) - set(files2.keys())
            unique2 = set(files2.keys()) - set(files1.keys())
            frame_mismatches = []

        # Export results with updated path information
        print("Exporting results...")
        export_method = getattr(Exporter, f'to_{args.format}')
        
        # Create display paths for multiple directories
        display_path1 = ' + '.join(dirs1) if len(dirs1) > 1 else dirs1[0]
        display_path2 = ' + '.join(dirs2) if len(dirs2) > 1 else dirs2[0]
        
        # Prepare data for export
        if args.adv:
            export_data = {
                'mode': 'proxy_advanced',
                'path1': display_path1,
                'path2': display_path2,
                'dirs1': dirs1,
                'dirs2': dirs2,
                'unique1': [files1[f]['path'] for f in unique1],
                'unique2': [files2[f]['path'] for f in unique2],
                'frame_mismatches': frame_mismatches
            }
        else:
            export_data = {
                'mode': args.mode,
                'path1': display_path1,
                'path2': display_path2,
                'dirs1': dirs1,
                'dirs2': dirs2,
                'unique1': [files1[f] for f in unique1],
                'unique2': [files2[f] for f in unique2]
            }
        
        export_method(export_data, output_path)

        print(f"\nResults have been exported to: {output_path}")
        print(f"Files only in group 1: {len(unique1)}")
        print(f"Files only in group 2: {len(unique2)}")
        if args.adv:
            print(f"Frame count mismatches: {len(frame_mismatches)}")
        print(f"Total execution time: {time.time() - start_time:.2f} seconds")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()