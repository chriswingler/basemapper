# BaseMapper

A powerful Python tool that maps your entire codebase into a single, navigable document. BaseMapper recursively traverses your project directory, creates a clean directory hierarchy, and includes the contents of all files not excluded in a .bmignore file.

## Features

- 📂 **Complete Directory Mapping** - Creates a hierarchical view of your entire codebase
- 📄 **File Content Inclusion** - Embeds the contents of all text files with syntax highlighting (Markdown) or plain text
- 🔍 **Smart Exclusions** - Uses .bmignore files (similar to .gitignore) to exclude files and directories
- 🎨 **Multiple Output Formats** - Generate both Markdown and plain text versions
- 🔗 **Navigation Links** - Markdown output includes clickable links for easy navigation
- 🔄 **Cross-Platform** - Works on Windows, macOS, and Linux

## Usage

```bash
python basemapper.py [directory_path] [output_file] [bmignore_file] [--raw]
```

### Parameters:

- `directory_path` - The directory to map (defaults to current working directory)
- `output_file` - The output file path (defaults to "codebase_map.md")
- `bmignore_file` - Path to a specific .bmignore file (optional)
- `--raw` - Generate a raw text version alongside the Markdown version

### Examples:

```bash
# Map the current directory to the default output file
python basemapper.py

# Map a specific directory to a custom output file
python basemapper.py /path/to/project project_map.md

# Use a specific .bmignore file and generate both Markdown and raw text
python basemapper.py /path/to/project project_map.md /path/to/custom.bmignore --raw
```

## Exclusion Patterns (.bmignore)

BaseMapper uses .bmignore files similar to .gitignore to exclude files and directories from the mapping. Example patterns:

```
# Exclude specific directories
build/
node_modules/

# Exclude file types
*.exe
*.dll
*.so

# Exclude specific files
secret_config.json
private_keys.txt

# Exclude files at any level
**/temp_files.txt
```

## Output Examples

### Markdown Output

The Markdown output includes:
- A clickable table of contents with directory structure
- Syntax-highlighted file contents
- Navigation links between sections

### Raw Text Output

The raw text output provides a minimal representation with:
- A clean directory tree structure
- Plain text file contents
- Smaller file size for easier sharing

## Why Use BaseMapper?

- **Code Reviews** - Share your entire codebase in a single, navigable document
- **Documentation** - Create comprehensive documentation of your project structure
- **Onboarding** - Help new team members understand the codebase quickly
- **Archiving** - Create a readable snapshot of your project at a specific point in time
- **Code Analysis** - Easily search and analyze patterns across your entire codebase

## Example Output

Here's a snippet of what the Markdown output looks like:

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

And here's what the raw text output looks like:

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

README.md
# MyProject
A sample project to demonstrate BaseMapper
...
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 