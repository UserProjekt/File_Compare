import json
import csv
import html
import os
from datetime import datetime

class Exporter:
    @staticmethod
    def _get_html_style():
        return """
            body { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                margin: 20px;
                line-height: 1.5;
                color: #333;
            }
            table { 
                border-collapse: collapse; 
                width: 100%; 
                margin-top: 10px;
                margin-bottom: 40px;
            }
            th, td { 
                border: 1px solid #ddd; 
                padding: 12px; 
                text-align: left;
                font-family: inherit;
            }
            th { 
                background-color: #f2f2f2;
                font-weight: 600;
            }
            .path1 { background-color: #ffeeee; }
            .path2 { background-color: #eeffee; }
            .path-header { 
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 6px;
                margin: 30px 0;
                border: 1px solid #ddd;
            }
            .path-header h3 {
                margin: 0 0 10px 0;
                font-size: 1.2em;
                color: #333;
            }
            .path-text {
                font-family: inherit;
                background-color: #fff;
                padding: 10px;
                border-radius: 4px;
                border: 1px solid #ddd;
                word-break: break-all;
                margin-bottom: 5px;
            }
            .section {
                margin-bottom: 40px;
            }
            .mode-info {
                background-color: #e9ecef;
                padding: 10px 20px;
                border-radius: 4px;
                margin-bottom: 20px;
                border: 1px solid #dee2e6;
                display: inline-block;
            }
            .dir-list {
                list-style-type: none;
                padding: 0;
                margin: 0;
            }
            .dir-list li {
                margin-bottom: 5px;
            }
        """

    @staticmethod
    def to_json(data, output_file):
        """Export results to JSON format"""
        results = {
            'mode': data['mode'],
            'comparison_time': datetime.now().isoformat(),
            'group1': {
                'directories': data.get('dirs1', [data['path1']]),
                'combined_path': data['path1']
            },
            'group2': {
                'directories': data.get('dirs2', [data['path2']]),
                'combined_path': data['path2']
            },
            'files_only_in_group1': data['unique1'],
            'files_only_in_group2': data['unique2']
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

    @staticmethod
    def to_txt(data, output_file):
        """Export results to text format"""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"File Comparison Results\n")
            f.write(f"Mode: {data['mode']}\n")
            f.write(f"Time: {datetime.now()}\n\n")
            
            # Group 1
            f.write(f"Files only in first group:\n")
            if 'dirs1' in data and len(data['dirs1']) > 1:
                f.write("Directories:\n")
                for dir_path in data['dirs1']:
                    f.write(f"  - {dir_path}\n")
            else:
                f.write(f"Directory: {data['path1']}\n")
            
            f.write(f"({len(data['unique1'])} files):\n")
            for file in sorted(data['unique1']):
                f.write(f"{file}\n")
            
            # Group 2
            f.write(f"\nFiles only in second group:\n")
            if 'dirs2' in data and len(data['dirs2']) > 1:
                f.write("Directories:\n")
                for dir_path in data['dirs2']:
                    f.write(f"  - {dir_path}\n")
            else:
                f.write(f"Directory: {data['path2']}\n")
            
            f.write(f"({len(data['unique2'])} files):\n")
            for file in sorted(data['unique2']):
                f.write(f"{file}\n")

    @staticmethod
    def to_csv(data, output_file):
        """Export results to CSV format"""
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:  # Changed to utf-8-sig for better Excel compatibility
            writer = csv.writer(f)
            writer.writerow(['Mode', data['mode']])
            writer.writerow(['Time', datetime.now()])
            writer.writerow([])
            
            # Write directory information
            writer.writerow(['Group 1 Directories'] + data.get('dirs1', [data['path1']]))
            writer.writerow(['Group 2 Directories'] + data.get('dirs2', [data['path2']]))
            writer.writerow([])
            
            writer.writerow(['Location', 'Path'])
            
            for file in sorted(data['unique1']):
                writer.writerow(['Group1', file])
            for file in sorted(data['unique2']):
                writer.writerow(['Group2', file])

    @staticmethod
    def to_html(data, output_file):
        """Export results to HTML format"""
        mode_description = ("Normal (comparing all files by basename.extension)" 
                           if data['mode'] == 'normal' 
                           else "Proxy (comparing video files by basename only)")
        
        # Format directory lists
        def format_dirs_html(dirs):
            if len(dirs) == 1:
                return f'<div class="path-text">{html.escape(dirs[0])}</div>'
            else:
                dir_items = ''.join(f'<div class="path-text">{html.escape(d)}</div>' for d in dirs)
                return f'{dir_items}'
        
        dirs1_html = format_dirs_html(data.get('dirs1', [data['path1']]))
        dirs2_html = format_dirs_html(data.get('dirs2', [data['path2']]))
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Comparison Results</title>
    <style>{Exporter._get_html_style()}</style>
</head>
<body>
    <h2>File Comparison Results</h2>
    <div class="mode-info">
        <strong>Mode:</strong> {mode_description}<br>
        <strong>Time:</strong> {datetime.now()}
    </div>
    
    <div class="section">
        <div class="path-header">
            <h3>Files only in first group: ({len(data['unique1'])} files)</h3>
            {dirs1_html}
        </div>
        <table>
            <tr><th>File Path</th></tr>
            {''.join(f'<tr class="path1"><td>{html.escape(f)}</td></tr>' for f in sorted(data['unique1']))}
        </table>
    </div>
    
    <div class="section">
        <div class="path-header">
            <h3>Files only in second group: ({len(data['unique2'])} files)</h3>
            {dirs2_html}
        </div>
        <table>
            <tr><th>File Path</th></tr>
            {''.join(f'<tr class="path2"><td>{html.escape(f)}</td></tr>' for f in sorted(data['unique2']))}
        </table>
    </div>
</body>
</html>"""
        
        # Write with UTF-8 BOM for better compatibility
        with open(output_file, 'wb') as f:
            # Write UTF-8 BOM
            f.write(b'\xef\xbb\xbf')
            # Write content as UTF-8
            f.write(html_content.encode('utf-8'))