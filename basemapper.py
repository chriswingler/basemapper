#!/usr/bin/env python3
r"""
BaseMapper.py - Maps directory structure and exports file contents to Markdown

This script recursively traverses a directory and:
1. Creates a clean directory hierarchy as a table of contents
2. Includes the contents of all non-binary files not excluded by .bmignore
3. Outputs everything to a single Markdown file for easy sharing and viewing

Usage:
  python basemapper.py [directory_path] [output_file] [bmignore_file] [--raw]

If no directory_path is specified, the current working directory will be used.
If no output_file is specified, "codebase_map.md" will be used.
If no bmignore_file is specified, the script will look for .bmignore in the current working directory.
If --raw is specified, a raw text version will also be generated alongside the Markdown version.

Paths can be:
  - Absolute (e.g., /path/to/directory or C:\path\to\directory)
  - Relative to the current working directory (e.g., ./subdirectory or ../parent_directory)

Exclusions:
  The script will look for a .bmignore file in the current working directory, which follows
  the same format as .gitignore. If not found, all files will be included.
  The following are always excluded regardless of .bmignore settings:
  - The output file itself
  - All .bmignore files
  - The basemapper.py script itself
"""

import os
import sys
import fnmatch
import pathlib
from typing import List, Tuple, Dict, Set, Optional, Any
from datetime import datetime


def parse_bmignore(root_dir: str, bmignore_path: Optional[str] = None) -> List[str]:
    """Parse .bmignore file and return patterns to ignore.
    
    Args:
        root_dir: The root directory being mapped
        bmignore_path: Optional path to a specific .bmignore file
    
    Returns:
        List of patterns to ignore
    """
    ignore_patterns = []
    
    # Priority 1: Use the specified .bmignore file if provided
    if bmignore_path and os.path.exists(bmignore_path):
        print(f"Using specified .bmignore file: {bmignore_path}")
        ignore_file = bmignore_path
    # Priority 2: Look for .bmignore in the current working directory
    elif os.path.exists(os.path.join(os.getcwd(), '.bmignore')):
        ignore_file = os.path.join(os.getcwd(), '.bmignore')
        print(f"Using .bmignore file from current directory: {ignore_file}")
    # Priority 3: Look for .bmignore in the target directory
    elif os.path.exists(os.path.join(root_dir, '.bmignore')):
        ignore_file = os.path.join(root_dir, '.bmignore')
        print(f"Using .bmignore file from target directory: {ignore_file}")
    else:
        print("No .bmignore file found. All files will be included.")
        return ignore_patterns
    
    # Parse the ignore file
    with open(ignore_file, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Handle directory patterns (ending with /)
                if line.endswith('/'):
                    line = line[:-1]
                
                # Add the pattern as-is (we'll handle the leading / in should_ignore)
                ignore_patterns.append(line)
    
    return ignore_patterns


def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary by reading its first few thousand bytes.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if the file is binary, False otherwise
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(4096)
            return b'\0' in chunk  # Binary files typically contain null bytes
    except (IOError, PermissionError):
        return True  # If we can't read it, treat as binary


def should_ignore(path: str, ignore_patterns: List[str], root_dir: str, output_file: str) -> bool:
    """Check if a path should be ignored based on ignore patterns.
    
    Args:
        path: Path to check
        ignore_patterns: List of patterns to ignore
        root_dir: Root directory being mapped
        output_file: Output file path
        
    Returns:
        True if the path should be ignored, False otherwise
    """
    # Get the absolute paths for comparison
    abs_path = os.path.abspath(path)
    abs_output_file = os.path.abspath(output_file)
    
    # Always ignore .bmignore files
    if os.path.basename(path) == '.bmignore':
        return True
    
    # Always ignore the output file itself
    if abs_path == abs_output_file:
        return True
    
    # Get the relative path for pattern matching
    rel_path = os.path.relpath(path, root_dir)
    
    # Check if path matches any ignore pattern
    for pattern in ignore_patterns:
        # Handle absolute patterns (starting with /)
        if pattern.startswith('/'):
            # Remove the leading / for matching
            pattern = pattern[1:]
            # Only match at the root level
            if fnmatch.fnmatch(rel_path, pattern):
                return True
        elif pattern.startswith('**/'):
            # Match pattern at any level
            basename = os.path.basename(path)
            if fnmatch.fnmatch(basename, pattern[3:]):
                return True
        else:
            # Match pattern at any level
            if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
                return True
            
    return False


def get_language_from_extension(file_path: str) -> str:
    """Determine the language based on file extension for markdown code blocks.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Language identifier for markdown code blocks
    """
    ext = os.path.splitext(file_path)[1].lower()
    
    # Map of extensions to markdown language identifiers
    language_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'jsx',
        '.tsx': 'tsx',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
        '.java': 'java',
        '.sh': 'bash',
        '.bat': 'batch',
        '.ps1': 'powershell',
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown',
        '.sql': 'sql',
        '.rb': 'ruby',
        '.go': 'go',
        '.php': 'php',
        '.cs': 'csharp',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.rs': 'rust',
        '.dart': 'dart',
        '.lua': 'lua',
        '.r': 'r',
        '.pl': 'perl',
        '.pm': 'perl',
        '.scala': 'scala',
        '.groovy': 'groovy',
        '.coffee': 'coffeescript',
        '.elm': 'elm',
        '.erl': 'erlang',
        '.hs': 'haskell',
        '.ex': 'elixir',
        '.exs': 'elixir',
        '.clj': 'clojure',
        '.fs': 'fsharp',
        '.fsx': 'fsharp',
        '.cmake': 'cmake',
        '.dockerfile': 'dockerfile',
        '.tf': 'terraform',
        '.vue': 'vue',
        '.svelte': 'svelte',
    }
    
    return language_map.get(ext, '')  # Return empty string if not found


def create_file_id(file_path: str) -> str:
    """Create a safe anchor ID for a file path.
    
    Args:
        file_path: Path to create an ID for
        
    Returns:
        A safe anchor ID for use in HTML/Markdown
    """
    # Replace problematic characters with underscores
    safe_id = file_path.replace('/', '_').replace('\\', '_')
    safe_id = safe_id.replace('.', '_').replace(' ', '_')
    safe_id = safe_id.replace('(', '_').replace(')', '_')
    safe_id = safe_id.replace('[', '_').replace(']', '_')
    safe_id = safe_id.replace('{', '_').replace('}', '_')
    safe_id = safe_id.replace(':', '_').replace(';', '_')
    safe_id = safe_id.replace(',', '_').replace('\'', '_')
    safe_id = safe_id.replace('"', '_').replace('`', '_')
    safe_id = safe_id.replace('!', '_').replace('@', '_')
    safe_id = safe_id.replace('#', '_').replace('$', '_')
    safe_id = safe_id.replace('%', '_').replace('^', '_')
    safe_id = safe_id.replace('&', '_').replace('*', '_')
    safe_id = safe_id.replace('+', '_').replace('=', '_')
    safe_id = safe_id.replace('|', '_').replace('~', '_')
    
    # Ensure the ID is lowercase for consistency and add a prefix to avoid conflicts
    return f"file_{safe_id.lower()}"


def generate_raw_text_version(root_dir: str, all_dirs: Set[str], all_files: List[Tuple[str, str]], output_file: str) -> None:
    """Generate a minimal raw text version of the codebase map.
    
    Args:
        root_dir: The root directory being mapped
        all_dirs: Set of all directories
        all_files: List of tuples (relative_path, absolute_path) for all files
        output_file: The output file path
    """
    # Create the raw text output file path by replacing the extension with .txt
    raw_output_file = os.path.splitext(output_file)[0] + ".txt"
    
    with open(raw_output_file, 'w', encoding='utf-8', errors='replace') as out:
        # Simple directory structure header
        out.write("DIRECTORY STRUCTURE:\n\n")
        
        # Create a sorted list of all directories including the root
        all_dirs_list = sorted(list(all_dirs))
        
        # Create a list of all files by relative path
        all_files_by_path = {rel_path: abs_path for rel_path, abs_path in all_files}
        
        # Build a complete tree structure
        tree = {}
        
        # Add all directories to the tree
        for dir_path in all_dirs_list:
            parts = dir_path.split(os.sep)
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        # Add all files to the tree
        for rel_file_path in sorted(all_files_by_path.keys()):
            parts = rel_file_path.split(os.sep)
            filename = parts[-1]
            dir_parts = parts[:-1]
            
            # Navigate to the correct directory
            current = tree
            for part in dir_parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
            
            # Add the file as a leaf (marked with None)
            current[filename] = None
        
        # Write the root directory
        root_name = os.path.basename(os.path.abspath(root_dir)) or os.path.abspath(root_dir)
        out.write(f"{root_name}\n")
        
        # Recursive function to print the tree
        def print_tree(node: Dict[str, Any], prefix: str = "", is_last: bool = True, path: str = "") -> None:
            items = sorted(node.items(), key=lambda x: (x[1] is not None, x[0]))
            for i, (name, subtree) in enumerate(items):
                is_last_item = i == len(items) - 1
                
                # Determine the current item's full path
                current_path = os.path.join(path, name) if path else name
                
                # Print the item with appropriate prefix
                if subtree is None:  # It's a file
                    out.write(f"{prefix}{'└── ' if is_last_item else '├── '}{name}\n")
                else:  # It's a directory
                    out.write(f"{prefix}{'└── ' if is_last_item else '├── '}{name}/\n")
                    
                    # Prepare the next prefix
                    next_prefix = prefix + ("    " if is_last_item else "│   ")
                    print_tree(subtree, next_prefix, is_last_item, current_path)
        
        # Print the tree starting from the root level
        print_tree(tree)
        
        # Add a separator before file contents
        out.write("\nFILE CONTENTS:\n\n")
        
        # Write all file contents with minimal formatting
        for rel_file_path, actual_file_path in sorted(all_files):
            if is_binary_file(actual_file_path):
                out.write(f"{rel_file_path} [BINARY]\n\n")
                continue
                
            try:
                with open(actual_file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                # Write the file path and content with minimal formatting
                out.write(f"{rel_file_path}\n")
                out.write(content)
                if not content.endswith('\n'):
                    out.write('\n')
                out.write('\n')
            except Exception as e:
                out.write(f"{rel_file_path} [ERROR: {str(e)}]\n\n")
    
    print(f"Raw text version saved to: {raw_output_file}")


def map_directory(root_dir: str, output_file: str, bmignore_path: Optional[str] = None, generate_raw: bool = False) -> None:
    """Map the directory structure and file contents to a markdown file.
    
    Args:
        root_dir: The directory to map
        output_file: The output file path
        bmignore_path: Optional path to a specific .bmignore file
        generate_raw: Whether to also generate a raw text version
    """
    # Ensure root_dir is an absolute path
    root_dir = os.path.abspath(root_dir)
    output_file = os.path.abspath(output_file)
    
    # Get the absolute path of the current script for exclusion
    script_path = os.path.abspath(__file__)
    
    # Parse .bmignore file
    ignore_patterns = parse_bmignore(root_dir, bmignore_path)
    
    # Track all directories and files first to create a clean hierarchical view
    all_dirs = set()
    all_files = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        rel_path = os.path.relpath(dirpath, root_dir)
        if rel_path == '.':
            rel_path = ''
            
        # Skip ignored directories
        if should_ignore(dirpath, ignore_patterns, root_dir, output_file):
            dirnames[:] = []  # Skip all subdirectories
            continue
            
        # Add this directory to our set
        if rel_path:
            all_dirs.add(rel_path)
            
        # Add all non-ignored files
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            abs_file_path = os.path.abspath(file_path)
            
            # Skip the script itself
            if abs_file_path == script_path:
                continue
                
            if not should_ignore(file_path, ignore_patterns, root_dir, output_file):
                rel_file_path = os.path.join(rel_path, filename) if rel_path else filename
                all_files.append((rel_file_path, file_path))
    
    # Create a dictionary to store file IDs to ensure consistency
    file_ids = {}
    for rel_file_path, _ in all_files:
        file_ids[rel_file_path] = create_file_id(rel_file_path)
    
    # Generate the Markdown version
    with open(output_file, 'w', encoding='utf-8', errors='replace') as out:
        # Write header
        out.write(f"# Codebase Map: {os.path.basename(root_dir)}\n\n")
        out.write(f"Generated by BaseMapper.py on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        out.write(f"Base directory: `{root_dir}`\n\n")
        out.write("---\n\n")
        
        # Print the table of contents with consistent file IDs
        out.write("# Directory Structure\n\n")
        
        # Display the root directory first
        root_name = os.path.basename(os.path.abspath(root_dir)) or os.path.abspath(root_dir)
        out.write(f"- 📂 **{root_name}** (ROOT)\n")
        
        # Create a nested dictionary structure for directories
        dir_tree = {}
        
        # Add all directories to the tree
        for dir_path in sorted(all_dirs):
            parts = dir_path.split(os.sep)
            current = dir_tree
            for part in parts:
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        # Files by directory
        files_by_dir = {}
        for rel_file_path, _ in all_files:
            dir_name = os.path.dirname(rel_file_path)
            if not dir_name:
                dir_name = ""  # Root
            if dir_name not in files_by_dir:
                files_by_dir[dir_name] = []
            files_by_dir[dir_name].append(rel_file_path)
        
        # Print root files
        if "" in files_by_dir:
            for rel_file_path in sorted(files_by_dir[""]):
                file_name = os.path.basename(rel_file_path)
                file_id = file_ids[rel_file_path]
                out.write(f"  - 📄 [{file_name}](#{file_id})\n")
        
        # Recursive function to print the directory tree
        def print_tree(tree: Dict[str, Any], path: str = "", indent: int = 1) -> None:
            for name in sorted(tree.keys()):
                full_path = os.path.join(path, name) if path else name
                out.write(f"{' ' * (indent * 2)}- 📁 **{name}/**\n")
                
                # Print files in this directory
                if full_path in files_by_dir:
                    for rel_file_path in sorted(files_by_dir[full_path]):
                        file_name = os.path.basename(rel_file_path)
                        file_id = file_ids[rel_file_path]
                        out.write(f"{' ' * ((indent + 1) * 2)}- 📄 [{file_name}](#{file_id})\n")
                
                # Recurse into subdirectories
                print_tree(tree[name], full_path, indent + 1)
        
        # Print the directory tree
        print_tree(dir_tree)
        
        out.write("\n---\n\n")
        
        # Output file contents
        out.write("# File Contents\n\n")
        
        for rel_file_path, actual_file_path in sorted(all_files, key=lambda f: f[0]):
            # Get the consistent file ID
            file_id = file_ids[rel_file_path]
            
            # Write file header
            out.write(f"<a id='{file_id}'></a>\n\n")
            out.write(f"## {rel_file_path}\n\n")
            
            if is_binary_file(actual_file_path):
                out.write("*[BINARY FILE - CONTENTS SKIPPED]*\n\n")
                continue
                
            try:
                with open(actual_file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                # Get language for syntax highlighting
                language = get_language_from_extension(rel_file_path)
                
                # Write file content with syntax highlighting
                out.write(f"```{language}\n")
                out.write(content)
                if not content.endswith('\n'):
                    out.write('\n')
                out.write("```\n\n")
                
            except Exception as e:
                out.write(f"*[ERROR: {str(e)}]*\n\n")
        
        # Summary
        out.write("# Summary\n\n")
        out.write(f"- **Total directories:** {len(all_dirs) + 1} (including root)\n")
        out.write(f"- **Total files:** {len(all_files)}\n")
        
    print(f"Directory mapping complete. Output saved to: {output_file}")
    print(f"Found {len(all_dirs) + 1} directories and {len(all_files)} files.")
    
    # Generate raw text version if requested
    if generate_raw:
        generate_raw_text_version(root_dir, all_dirs, all_files, output_file)


def main() -> None:
    """Main entry point for the script."""
    # Check for --raw flag
    generate_raw = False
    args = sys.argv[:]
    if "--raw" in args:
        generate_raw = True
        args.remove("--raw")
    
    # Get directory to map
    if len(args) > 1:
        # Handle the provided directory path - all paths are relative to CWD
        directory = os.path.abspath(args[1])
    else:
        # Default to the current working directory
        directory = os.getcwd()
    
    # Get output file name (use default if not specified)
    if len(args) > 2:
        # Output file is relative to CWD
        output_file = os.path.abspath(args[2])
    else:
        # Default output file in CWD
        output_file = os.path.join(os.getcwd(), "codebase_map.md")
    
    # Get optional .bmignore file path
    bmignore_path = None
    if len(args) > 3:
        bmignore_path = os.path.abspath(args[3])
    
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        sys.exit(1)
    
    print(f"Mapping directory: {directory}")
    
    map_directory(directory, output_file, bmignore_path, generate_raw)


if __name__ == "__main__":
    main() 