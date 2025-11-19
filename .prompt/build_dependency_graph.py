#!/usr/bin/env python3
"""
Dependency Graph Builder for Crawl4AI Repository

Scans the repository and extracts:
- Imports and exports
- Class references and inheritance
- Identifier references
- File relationships

Outputs to: .prompt/dependency-graph.json
"""

import os
import json
import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import sys

# Files and directories to exclude
EXCLUDE_DIRS = {
    '.git', '__pycache__', 'node_modules', '.pytest_cache',
    '.mypy_cache', 'dist', 'build', '*.egg-info', 'venv',
    'env', '.venv', '.env'
}

EXCLUDE_FILES = {
    '.DS_Store', 'Thumbs.db', '*.pyc', '*.pyo', '*.pyd',
    '*.so', '*.dll', '*.dylib', '*.zip', '*.tar.gz'
}

# File extensions to process
FILE_EXTENSIONS = {
    '.py', '.js', '.ts', '.tsx', '.jsx', '.go', '.cs',
    '.sql', '.yaml', '.yml', '.json', '.html', '.css',
    '.sh', '.md', '.toml', '.ini', '.cfg'
}


class DependencyGraphBuilder:
    """Build a comprehensive dependency graph of the repository."""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.graph: Dict[str, Any] = {
            'metadata': {
                'root_path': str(self.root_path),
                'total_files': 0,
                'file_types': defaultdict(int),
            },
            'files': {}
        }
        self.stats = defaultdict(int)

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        # Check directory exclusions
        for part in path.parts:
            if part in EXCLUDE_DIRS or part.startswith('.'):
                return True

        # Check file exclusions
        if path.name in EXCLUDE_FILES:
            return True

        return False

    def get_relative_path(self, path: Path) -> str:
        """Get path relative to root."""
        try:
            return str(path.relative_to(self.root_path))
        except ValueError:
            return str(path)

    def scan_repository(self):
        """Scan the entire repository and build dependency graph."""
        print(f"🔍 Scanning repository: {self.root_path}")

        for root, dirs, files in os.walk(self.root_path):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]

            root_path = Path(root)

            for filename in files:
                file_path = root_path / filename

                if self.should_exclude(file_path):
                    continue

                ext = file_path.suffix.lower()
                if ext not in FILE_EXTENSIONS:
                    continue

                rel_path = self.get_relative_path(file_path)

                try:
                    self.process_file(file_path, rel_path, ext)
                    self.stats['processed'] += 1
                except Exception as e:
                    self.stats['errors'] += 1
                    print(f"⚠️  Error processing {rel_path}: {e}")

        self.finalize_graph()

    def process_file(self, file_path: Path, rel_path: str, ext: str):
        """Process a single file based on its type."""
        self.graph['metadata']['total_files'] += 1
        self.graph['metadata']['file_types'][ext] += 1

        file_info = {
            'path': rel_path,
            'type': ext,
            'size': file_path.stat().st_size,
            'imports': [],
            'exports': [],
            'classes': [],
            'functions': [],
            'identifiers': [],
            'dependencies': [],
            'dependents': []
        }

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            if ext == '.py':
                self.process_python(content, file_info)
            elif ext in {'.js', '.ts', '.tsx', '.jsx'}:
                self.process_javascript(content, file_info)
            elif ext in {'.yaml', '.yml'}:
                self.process_yaml(content, file_info)
            elif ext == '.json':
                self.process_json(content, file_info)
            elif ext == '.html':
                self.process_html(content, file_info)
            elif ext == '.go':
                self.process_go(content, file_info)
            elif ext == '.cs':
                self.process_csharp(content, file_info)
            elif ext == '.sql':
                self.process_sql(content, file_info)
            elif ext == '.md':
                self.process_markdown(content, file_info)

        except Exception as e:
            print(f"  Error reading {rel_path}: {e}")
            file_info['error'] = str(e)

        self.graph['files'][rel_path] = file_info

    def process_python(self, content: str, file_info: Dict):
        """Process Python file using AST."""
        try:
            tree = ast.parse(content)

            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        import_info = {
                            'module': alias.name,
                            'alias': alias.asname,
                            'type': 'import'
                        }
                        file_info['imports'].append(import_info)
                        file_info['dependencies'].append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        import_info = {
                            'module': module,
                            'name': alias.name,
                            'alias': alias.asname,
                            'type': 'from_import'
                        }
                        file_info['imports'].append(import_info)
                        if module:
                            file_info['dependencies'].append(module)

                # Extract class definitions
                elif isinstance(node, ast.ClassDef):
                    class_info = {
                        'name': node.name,
                        'bases': [self.get_name(base) for base in node.bases],
                        'decorators': [self.get_name(dec) for dec in node.decorator_list],
                        'methods': [],
                        'line': node.lineno
                    }

                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                'name': item.name,
                                'args': [arg.arg for arg in item.args.args],
                                'decorators': [self.get_name(dec) for dec in item.decorator_list],
                                'line': item.lineno
                            }
                            class_info['methods'].append(method_info)

                    file_info['classes'].append(class_info)

                # Extract function definitions
                elif isinstance(node, ast.FunctionDef):
                    # Only top-level functions
                    if isinstance(getattr(node, 'parent', None), ast.Module) or not hasattr(node, 'parent'):
                        func_info = {
                            'name': node.name,
                            'args': [arg.arg for arg in node.args.args],
                            'decorators': [self.get_name(dec) for dec in node.decorator_list],
                            'line': node.lineno,
                            'is_async': isinstance(node, ast.AsyncFunctionDef)
                        }
                        file_info['functions'].append(func_info)

            # Add parent references for context
            for node in ast.walk(tree):
                for child in ast.iter_child_nodes(node):
                    child.parent = node

        except SyntaxError as e:
            file_info['parse_error'] = f"Syntax error: {e}"

    def process_javascript(self, content: str, file_info: Dict):
        """Process JavaScript/TypeScript file using regex."""
        # Import patterns
        import_patterns = [
            r'import\s+(?:(?P<default>\w+)|{\s*(?P<named>[^}]+)\s*}|(?P<star>\*\s+as\s+\w+))\s+from\s+["\'](?P<module>[^"\']+)["\']',
            r'import\s+["\'](?P<module>[^"\']+)["\']',
            r'require\(["\'](?P<module>[^"\']+)["\']\)',
        ]

        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                module = match.group('module') if 'module' in match.groupdict() else None
                if module:
                    import_info = {
                        'module': module,
                        'type': 'import'
                    }
                    if 'default' in match.groupdict() and match.group('default'):
                        import_info['default'] = match.group('default')
                    if 'named' in match.groupdict() and match.group('named'):
                        import_info['named'] = [n.strip() for n in match.group('named').split(',')]

                    file_info['imports'].append(import_info)
                    file_info['dependencies'].append(module)

        # Export patterns
        export_patterns = [
            r'export\s+default\s+(?:class\s+)?(?P<name>\w+)',
            r'export\s+(?:class|function|const|let|var)\s+(?P<name>\w+)',
            r'export\s+{\s*(?P<names>[^}]+)\s*}',
        ]

        for pattern in export_patterns:
            for match in re.finditer(pattern, content):
                if 'name' in match.groupdict() and match.group('name'):
                    file_info['exports'].append({'name': match.group('name')})
                elif 'names' in match.groupdict() and match.group('names'):
                    for name in match.group('names').split(','):
                        file_info['exports'].append({'name': name.strip()})

        # Class definitions
        class_pattern = r'class\s+(?P<name>\w+)(?:\s+extends\s+(?P<base>\w+))?'
        for match in re.finditer(class_pattern, content):
            class_info = {
                'name': match.group('name'),
                'bases': [match.group('base')] if match.group('base') else []
            }
            file_info['classes'].append(class_info)

        # Function definitions
        func_patterns = [
            r'function\s+(?P<name>\w+)\s*\(',
            r'const\s+(?P<name>\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
            r'async\s+function\s+(?P<name>\w+)\s*\(',
        ]

        for pattern in func_patterns:
            for match in re.finditer(pattern, content):
                func_info = {
                    'name': match.group('name'),
                    'is_async': 'async' in match.group(0)
                }
                file_info['functions'].append(func_info)

    def process_yaml(self, content: str, file_info: Dict):
        """Process YAML file."""
        # Look for references to other files or modules
        file_refs = re.findall(r'(?:file|path|import):\s*["\']?([^"\'\s]+)["\']?', content, re.IGNORECASE)
        for ref in file_refs:
            file_info['dependencies'].append(ref)

    def process_json(self, content: str, file_info: Dict):
        """Process JSON file."""
        try:
            data = json.loads(content)

            # Look for dependencies in package.json
            if isinstance(data, dict):
                if 'dependencies' in data:
                    file_info['dependencies'].extend(data['dependencies'].keys())
                if 'devDependencies' in data:
                    file_info['dependencies'].extend(data['devDependencies'].keys())
                if 'imports' in data:
                    if isinstance(data['imports'], dict):
                        file_info['dependencies'].extend(data['imports'].keys())
        except json.JSONDecodeError:
            pass

    def process_html(self, content: str, file_info: Dict):
        """Process HTML file."""
        # Script tags
        script_pattern = r'<script[^>]*src=["\']([^"\']+)["\']'
        for match in re.finditer(script_pattern, content):
            file_info['dependencies'].append(match.group(1))

        # Link tags (CSS)
        link_pattern = r'<link[^>]*href=["\']([^"\']+\.css)["\']'
        for match in re.finditer(link_pattern, content):
            file_info['dependencies'].append(match.group(1))

        # Inline script imports
        inline_imports = re.findall(r'import\s+.+\s+from\s+["\']([^"\']+)["\']', content)
        file_info['dependencies'].extend(inline_imports)

    def process_go(self, content: str, file_info: Dict):
        """Process Go file."""
        # Package declaration
        package_match = re.search(r'package\s+(\w+)', content)
        if package_match:
            file_info['package'] = package_match.group(1)

        # Imports
        import_pattern = r'import\s+(?:"([^"]+)"|(\([^)]+\)))'
        for match in re.finditer(import_pattern, content):
            if match.group(1):
                file_info['imports'].append({'module': match.group(1)})
                file_info['dependencies'].append(match.group(1))
            elif match.group(2):
                # Multi-line import
                imports = re.findall(r'"([^"]+)"', match.group(2))
                for imp in imports:
                    file_info['imports'].append({'module': imp})
                    file_info['dependencies'].append(imp)

        # Struct definitions (similar to classes)
        struct_pattern = r'type\s+(\w+)\s+struct'
        for match in re.finditer(struct_pattern, content):
            file_info['classes'].append({'name': match.group(1), 'type': 'struct'})

        # Function definitions
        func_pattern = r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\('
        for match in re.finditer(func_pattern, content):
            file_info['functions'].append({'name': match.group(1)})

    def process_csharp(self, content: str, file_info: Dict):
        """Process C# file."""
        # Using directives
        using_pattern = r'using\s+(?:static\s+)?([^;]+);'
        for match in re.finditer(using_pattern, content):
            namespace = match.group(1).strip()
            file_info['imports'].append({'namespace': namespace})
            file_info['dependencies'].append(namespace)

        # Class definitions
        class_pattern = r'(?:public|private|protected|internal)?\s*(?:static|abstract|sealed)?\s*class\s+(\w+)(?:\s*:\s*([^{]+))?'
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            bases = []
            if match.group(2):
                bases = [b.strip() for b in match.group(2).split(',')]
            file_info['classes'].append({'name': class_name, 'bases': bases})

        # Method definitions
        method_pattern = r'(?:public|private|protected|internal)\s+(?:static\s+)?(?:async\s+)?(?:\w+\??)\s+(\w+)\s*\('
        for match in re.finditer(method_pattern, content):
            file_info['functions'].append({'name': match.group(1)})

    def process_sql(self, content: str, file_info: Dict):
        """Process SQL file."""
        # Table references in CREATE, ALTER, DROP
        table_pattern = r'(?:CREATE|ALTER|DROP)\s+TABLE\s+(?:IF\s+(?:NOT\s+)?EXISTS\s+)?([`\w.]+)'
        for match in re.finditer(table_pattern, content, re.IGNORECASE):
            table_name = match.group(1).strip('`')
            file_info['identifiers'].append({'name': table_name, 'type': 'table'})

        # Table references in SELECT, INSERT, UPDATE, DELETE
        from_pattern = r'FROM\s+([`\w.]+)'
        for match in re.finditer(from_pattern, content, re.IGNORECASE):
            table_name = match.group(1).strip('`')
            file_info['dependencies'].append(table_name)

    def process_markdown(self, content: str, file_info: Dict):
        """Process Markdown file."""
        # Links to other files
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for match in re.finditer(link_pattern, content):
            link_target = match.group(2)
            # Only include relative file links
            if not link_target.startswith(('http://', 'https://', '#')):
                file_info['dependencies'].append(link_target)

        # Code block language references
        code_pattern = r'```(\w+)'
        languages = set(re.findall(code_pattern, content))
        file_info['languages'] = list(languages)

    def get_name(self, node) -> str:
        """Extract name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self.get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self.get_name(node.func)
        else:
            return str(node)

    def finalize_graph(self):
        """Finalize the dependency graph by computing reverse dependencies."""
        print("\n📊 Building reverse dependencies...")

        # Build reverse dependencies
        for file_path, file_info in self.graph['files'].items():
            for dep in file_info.get('dependencies', []):
                # Try to resolve the dependency to an actual file
                resolved = self.resolve_dependency(file_path, dep)
                if resolved and resolved in self.graph['files']:
                    if file_path not in self.graph['files'][resolved]['dependents']:
                        self.graph['files'][resolved]['dependents'].append(file_path)

        # Add statistics
        self.graph['metadata']['statistics'] = {
            'total_files_processed': self.stats['processed'],
            'errors': self.stats['errors'],
            'total_imports': sum(len(f.get('imports', [])) for f in self.graph['files'].values()),
            'total_classes': sum(len(f.get('classes', [])) for f in self.graph['files'].values()),
            'total_functions': sum(len(f.get('functions', [])) for f in self.graph['files'].values()),
        }

        # Summary by file type
        print("\n📁 File type summary:")
        for ext, count in sorted(self.graph['metadata']['file_types'].items()):
            print(f"  {ext}: {count} files")

    def resolve_dependency(self, source_file: str, dep: str) -> Optional[str]:
        """Resolve a dependency string to an actual file path."""
        # For Python imports
        if '.' in dep and not dep.startswith('.'):
            # Try to map to file path
            dep_path = dep.replace('.', '/') + '.py'
            if dep_path in self.graph['files']:
                return dep_path

        # For relative imports
        if dep.startswith('.'):
            source_dir = str(Path(source_file).parent)
            # Handle relative path
            resolved = str(Path(source_dir) / dep)
            if resolved in self.graph['files']:
                return resolved

        return None

    def save_graph(self, output_path: str):
        """Save the dependency graph to JSON file."""
        print(f"\n💾 Saving dependency graph to: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.graph, f, indent=2, default=str)

        file_size = Path(output_path).stat().st_size
        print(f"✅ Saved {file_size:,} bytes")

    def print_summary(self):
        """Print summary statistics."""
        print("\n" + "="*60)
        print("📈 DEPENDENCY GRAPH SUMMARY")
        print("="*60)
        print(f"Total files processed: {self.stats['processed']}")
        print(f"Errors encountered: {self.stats['errors']}")
        print(f"Total imports: {self.graph['metadata']['statistics']['total_imports']}")
        print(f"Total classes: {self.graph['metadata']['statistics']['total_classes']}")
        print(f"Total functions: {self.graph['metadata']['statistics']['total_functions']}")
        print("="*60)


def main():
    """Main entry point."""
    # Get repository root (parent of .prompt directory)
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    print("🚀 Crawl4AI Dependency Graph Builder")
    print(f"📂 Repository: {repo_root}")
    print(f"🎯 Output: .prompt/dependency-graph.json")
    print()

    # Build the graph
    builder = DependencyGraphBuilder(str(repo_root))
    builder.scan_repository()

    # Save to JSON
    output_path = script_path.parent / 'dependency-graph.json'
    builder.save_graph(str(output_path))

    # Print summary
    builder.print_summary()

    print("\n✨ Done!")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
