# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BaseMapper is a Python tool that maps entire codebases into a single, navigable document. It's designed as a single-file application using only Python standard library dependencies.

## Architecture

The project follows a single-file design pattern with all functionality contained in `basemapper.py`:

- **File Traversal**: `walk_directory()` recursively scans directories while respecting `.bmignore` patterns
- **Pattern Matching**: `PathMatcher` class implements gitignore-style pattern matching
- **Output Generation**: `write_output()` creates formatted Markdown or plain text documents
- **Binary Detection**: `is_binary()` checks file headers to skip binary files
- **Syntax Highlighting**: `get_language()` maps file extensions to 40+ supported languages

## Key Commands

### Installation
```bash
# Standard installation
pip install .

# Development installation (editable)
pip install -e .

# From PyPI (when published)
pip install basemapper
```

### Running BaseMapper
```bash
# Basic usage (creates output.md in current directory)
basemapper

# Specify custom paths
basemapper /path/to/project -o custom_output.md

# Plain text output
basemapper -f plain

# Include hidden files
basemapper --hidden
```

### Testing
```bash
# Run all tests
python -m unittest test_basemapper.py

# Run specific test
python -m unittest test_basemapper.BaseMapperTestCase.test_create_file_id

# Run with verbose output
python -m unittest test_basemapper.py -v
```

## Configuration

### .bmignore File
Uses gitignore syntax to exclude files/directories. Default patterns include:
- Version control directories (.git, .svn, etc.)
- Build artifacts (__pycache__, *.pyc, dist/, build/)
- IDE files (.vscode, .idea)
- Binary files (detected automatically)

### pyproject.toml
Defines package metadata and build configuration using setuptools. Key sections:
- `[project]`: Package name, version, dependencies
- `[project.scripts]`: CLI entry point configuration
- `[build-system]`: Uses setuptools for building

## Development Guidelines

### Code Style
- Uses Python standard library only - no external dependencies
- Functions follow clear single-responsibility principle
- Comprehensive docstrings for all functions
- Type hints would be beneficial for clarity

### Adding Features
1. Maintain single-file design in `basemapper.py`
2. Ensure cross-platform compatibility (Windows, Linux, macOS)
3. Test with various repository structures
4. Update CLI help text in `argparse` configuration

### Common Tasks

**Add new language support**:
Edit the `LANGUAGE_MAP` dictionary in `basemapper.py`:
```python
LANGUAGE_MAP = {
    '.newext': 'newlang',
    # ...
}
```

**Modify default ignore patterns**:
Edit `DEFAULT_IGNORE_PATTERNS` list in `basemapper.py`

**Change output format**:
Modify `write_output()` function to add new format options

## Testing Approach

Current tests use Python's built-in `unittest` framework. Tests are in `test_basemapper.py`:
- Focus on unit testing individual functions
- Currently tests `create_file_id()` function
- Expand coverage for `PathMatcher`, `walk_directory()`, and output generation

## Project Structure

```
basemapper/
├── basemapper.py          # Main application code
├── test_basemapper.py     # Unit tests
├── pyproject.toml         # Package configuration
├── .bmignore             # Default ignore patterns
├── README.md             # User documentation
└── LICENSE               # MIT license
```

## Important Notes

- The tool processes text files only, automatically detecting and skipping binary files
- Memory efficient: processes files line by line
- Respects symbolic links but doesn't follow them
- Output includes file IDs for easy navigation in large documents