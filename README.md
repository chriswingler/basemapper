# BaseMapper

A powerful Python tool that maps your entire codebase into a single, navigable document. BaseMapper recursively traverses your project directory, creates a clean directory hierarchy, and includes the contents of all files not excluded in a .bmignore file.

## Features

- 📂 **Complete Directory Mapping** - Creates a hierarchical view of your entire codebase
- 📄 **File Content Inclusion** - Embeds the contents of all text files in plain text or with syntax highlighting (Markdown)
- 🔍 **Smart Exclusions** - Uses .bmignore files (similar to .gitignore) to exclude files and directories
- 🎨 **Multiple Output Formats** - Generate raw text (default) or Markdown output
- 🗣️ **Interactive Confirmation** - Prompts for confirmation before processing
- 🌐 **Language Support** - Syntax highlighting for 40+ programming languages in Markdown mode
- 🔗 **Navigation Links** - Markdown output includes clickable links for easy navigation
- 🔄 **Cross-Platform** - Works on Windows, macOS, and Linux

## Installation

BaseMapper can be installed in several ways depending on your system configuration and preferences.

### Option 1: Using pipx (Recommended for Local Installation)

[pipx](https://pypa.github.io/pipx/) is the recommended way to install Python applications locally. It automatically manages virtual environments and makes the command available globally:

```bash
# Install pipx if not already installed
sudo apt install pipx  # On Ubuntu/Debian
# or
brew install pipx      # On macOS
# or
pip install --user pipx  # Cross-platform

# Install BaseMapper from the local directory
pipx install .
```

After installation, `basemapper` will be available globally in your terminal.

### Option 2: Using Virtual Environment

If you encounter "externally-managed-environment" errors (common on modern Linux systems), use a virtual environment:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
# or
venv\Scripts\activate     # On Windows

# Install BaseMapper
pip install .

# Use the tool
basemapper [options]

# Or run directly without activation
./venv/bin/basemapper [options]  # Linux/macOS
venv\Scripts\basemapper [options]  # Windows
```

### Option 3: System-wide Installation

⚠️ **Warning**: Only use this if you understand the implications and your system allows it.

```bash
pip install .
```

If you get an "externally-managed-environment" error, you can override it (not recommended):

```bash
pip install . --break-system-packages
```

### Development Installation

For development, install in editable mode using any of the above methods:

```bash
# With pipx
pipx install -e .

# With virtual environment
pip install -e .
```

## Usage

After installation, you can run BaseMapper directly from your terminal:

```bash
basemapper [directory_path] [output_file] [bmignore_file] [--md]
```

You can also run the script directly (if you haven't installed the package or for development purposes):
```bash
python basemapper.py [directory_path] [output_file] [bmignore_file] [--md]
```

### Parameters:

- `directory_path` - The directory to map (defaults to current working directory)
- `output_file` - The output file path (defaults to "codebase_map.txt" for raw text, "codebase_map.md" for markdown)
- `bmignore_file` - Path to a specific .bmignore file (optional)
- `--md` - Generate Markdown output instead of the default raw text format

**Note**: BaseMapper will prompt for confirmation before processing the directory.

### Examples:

Using the installed command:
```bash
# Map the current directory to the default output file (codebase_map.txt)
basemapper

# Map a specific directory to a custom output file (raw text format)
basemapper /path/to/project project_map.txt

# Generate Markdown output instead of raw text
basemapper /path/to/project project_map.md --md

# Use a specific .bmignore file with Markdown output
basemapper /path/to/project project_map.md /path/to/custom.bmignore --md
```

## Exclusion Patterns (.bmignore)

BaseMapper uses .bmignore files similar to .gitignore to exclude files and directories from the mapping. A comprehensive default .bmignore file is included with common patterns for:

- **Version control**: `.git/`, `.svn/`, etc.
- **Build artifacts**: `__pycache__/`, `*.pyc`, `dist/`, `build/`
- **Dependencies**: `node_modules/`, `venv/`, virtual environments
- **IDE files**: `.vscode/`, `.idea/`, `*.swp`
- **Binary files**: executables, libraries, media files
- **Large data files**: `*.csv`, `*.pkl`, databases
- **Temporary files**: `*.tmp`, `*.bak`, `.cache/`
- **Security-sensitive files**: `.env`, `*.key`, `*.pem`

Example custom patterns:
```
# Exclude specific directories
custom_build/
legacy_code/

# Exclude file patterns
*.custom
test_*.json

# Exclude files at any level
**/generated_*.py
```

## Output Examples

### Raw Text Output (Default)

By default, BaseMapper generates a `.txt` file with:
- A clean ASCII directory tree structure
- Plain text file contents without formatting
- Smaller file size for easier sharing and processing
- No special formatting or syntax highlighting

### Markdown Output (with --md flag)

The Markdown output (`.md` file) includes:
- A clickable table of contents with emoji icons
- Syntax-highlighted code blocks for 40+ languages
- Navigation links between file sections
- Professional documentation-style formatting

## Why Use BaseMapper?

- **Code Reviews** - Share your entire codebase in a single, navigable document
- **Documentation** - Create comprehensive documentation of your project structure
- **Onboarding** - Help new team members understand the codebase quickly
- **Archiving** - Create a readable snapshot of your project at a specific point in time
- **Code Analysis** - Easily search and analyze patterns across your entire codebase

## Example Output

Here's what the default raw text output looks like:

```
DIRECTORY STRUCTURE:

MyProject
├── .gitignore
├── README.md
├── src/
│   ├── main.py
│   └── utils/
│       └── helpers.py

FILE CONTENTS:

.gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
...
```

And here's a snippet of what the Markdown output looks like (with `--md` flag):

```markdown
# Codebase Map: MyProject

Generated by BaseMapper.py on 2023-03-15 17:57:43

Base directory: `/path/to/MyProject`

---

# Directory Structure

- 📂 **MyProject** (ROOT)
  - 📄 [.gitignore](#file__gitignore)
  - 📄 [README.md](#file_readme_md)
  - 📁 **src/**
    - 📄 [main.py](#file_src_main_py)
    - 📁 **utils/**
      - 📄 [helpers.py](#file_src_utils_helpers_py)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.