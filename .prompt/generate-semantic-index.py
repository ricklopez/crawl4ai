#!/usr/bin/env python3
"""
Semantic Index Generator for Crawl4AI Repository

Processes dependency graph and IR files (when available) to generate:
- Domain clusters
- Dependency cycle detection
- System architecture mapping
- Priority groups for migration
- File index with metadata
- Migration groupings
- Database schema candidates

Outputs to: .prompt/semantic-index.md
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional
from collections import defaultdict, Counter
import re


class SemanticIndexGenerator:
    """Generate semantic index from dependency graph and IR files."""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path).resolve()
        self.prompt_dir = self.root_path / '.prompt'
        self.ir_dir = self.prompt_dir / 'ir'
        self.dep_graph_path = self.prompt_dir / 'dependency-graph.json'

        self.graph = None
        self.ir_files = {}
        self.clusters = defaultdict(list)
        self.cycles = []
        self.priority_groups = defaultdict(list)
        self.db_candidates = []

    def load_data(self):
        """Load dependency graph and IR files."""
        print("📂 Loading dependency graph...")
        if self.dep_graph_path.exists():
            with open(self.dep_graph_path, 'r', encoding='utf-8') as f:
                self.graph = json.load(f)
            print(f"✅ Loaded {len(self.graph['files'])} files from dependency graph")
        else:
            print("⚠️  No dependency graph found. Run build_dependency_graph.py first.")
            self.graph = {'files': {}, 'metadata': {}}

        print("\n📂 Loading IR files...")
        if self.ir_dir.exists():
            ir_count = 0
            for ir_file in self.ir_dir.rglob('*.md'):
                rel_path = ir_file.relative_to(self.ir_dir)
                self.ir_files[str(rel_path)] = self.parse_ir_file(ir_file)
                ir_count += 1
            print(f"✅ Loaded {ir_count} IR files")
        else:
            print("ℹ️  No IR files found yet. Index will be based on dependency graph only.")

    def parse_ir_file(self, ir_path: Path) -> Dict:
        """Parse an IR markdown file to extract metadata."""
        content = ir_path.read_text(encoding='utf-8')

        ir_data = {
            'path': str(ir_path),
            'purpose': '',
            'domain_role': '',
            'tags': []
        }

        # Extract purpose
        purpose_match = re.search(r'## 1\. Purpose\s+(.*?)(?=##|\Z)', content, re.DOTALL)
        if purpose_match:
            ir_data['purpose'] = purpose_match.group(1).strip()[:200]

        # Extract domain role
        domain_match = re.search(r'## 2\. Domain Role\s+(.*?)(?=##|\Z)', content, re.DOTALL)
        if domain_match:
            ir_data['domain_role'] = domain_match.group(1).strip()[:200]

        # Extract tags
        tags_match = re.search(r'## 14\. Tags\s+(.*?)(?=##|\Z)', content, re.DOTALL)
        if tags_match:
            tags_text = tags_match.group(1)
            # Extract bullet points or comma-separated tags
            ir_data['tags'] = re.findall(r'[-*]\s*(\S+)', tags_text) or \
                             [t.strip() for t in tags_text.split(',') if t.strip()]

        return ir_data

    def detect_domain_clusters(self):
        """Cluster files by domain based on path and dependencies."""
        print("\n🔍 Detecting domain clusters...")

        # Path-based clustering
        for file_path, file_info in self.graph['files'].items():
            if file_info['type'] != '.py':
                continue

            path_parts = Path(file_path).parts

            # Assign to domain based on path structure
            if 'crawl4ai' in path_parts:
                idx = path_parts.index('crawl4ai')
                if len(path_parts) > idx + 1:
                    subdomain = path_parts[idx + 1]

                    # Map to domain
                    if subdomain in ['deep_crawling', 'crawlers']:
                        self.clusters['Crawling Engine'].append(file_path)
                    elif subdomain in ['extraction_strategy', 'content_filter_strategy',
                                      'content_scraping_strategy']:
                        self.clusters['Content Processing'].append(file_path)
                    elif subdomain in ['models', 'types', 'async_configs']:
                        self.clusters['Core Models'].append(file_path)
                    elif subdomain in ['browser_manager', 'browser_profiler', 'browser_adapter']:
                        self.clusters['Browser Management'].append(file_path)
                    elif subdomain in ['async_dispatcher', 'async_logger', 'async_database']:
                        self.clusters['Infrastructure'].append(file_path)
                    elif subdomain == 'legacy':
                        self.clusters['Legacy Code'].append(file_path)
                    elif subdomain == 'components':
                        self.clusters['Shared Components'].append(file_path)
                    else:
                        self.clusters['Core Library'].append(file_path)
                else:
                    self.clusters['Core Library'].append(file_path)

            elif 'deploy/docker' in file_path:
                if 'static' in path_parts:
                    self.clusters['Frontend'].append(file_path)
                elif 'tests' in path_parts:
                    self.clusters['Docker Tests'].append(file_path)
                else:
                    self.clusters['API Server'].append(file_path)

            elif 'docs/md_v2/apps' in file_path:
                if 'crawl4ai-assistant' in file_path:
                    self.clusters['Chrome Extension'].append(file_path)
                else:
                    self.clusters['Web Apps'].append(file_path)

            elif 'tests' in path_parts:
                self.clusters['Test Suite'].append(file_path)

            elif 'docs' in path_parts:
                self.clusters['Documentation'].append(file_path)

        print(f"✅ Identified {len(self.clusters)} domain clusters")

    def detect_dependency_cycles(self):
        """Detect circular dependencies using DFS."""
        print("\n🔄 Detecting dependency cycles...")

        # Build adjacency list from dependency graph
        adj_list = defaultdict(set)
        for file_path, file_info in self.graph['files'].items():
            for dep in file_info.get('dependencies', []):
                # Try to resolve to actual file
                dep_file = self.resolve_dependency(file_path, dep)
                if dep_file:
                    adj_list[file_path].add(dep_file)

        # DFS to detect cycles
        visited = set()
        rec_stack = set()
        path = []

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in adj_list.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Found a cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    self.cycles.append(cycle)
                    return True

            path.pop()
            rec_stack.remove(node)
            return False

        for node in adj_list:
            if node not in visited:
                dfs(node)

        print(f"✅ Found {len(self.cycles)} dependency cycles")

    def resolve_dependency(self, source_file: str, dep: str) -> Optional[str]:
        """Resolve dependency string to actual file path."""
        # For Python module imports
        if '.' in dep and not dep.startswith('.'):
            # Try crawl4ai.* imports
            if dep.startswith('crawl4ai.'):
                dep_path = dep.replace('.', '/') + '.py'
                if dep_path in self.graph['files']:
                    return dep_path

            # Try generic module to path
            dep_path = dep.replace('.', '/') + '.py'
            if dep_path in self.graph['files']:
                return dep_path

        # For relative imports/paths
        if dep.startswith('.'):
            source_dir = str(Path(source_file).parent)
            resolved = str(Path(source_dir) / dep)
            if resolved in self.graph['files']:
                return resolved

        return None

    def map_system_architecture(self) -> Dict[str, Any]:
        """Map the overall system architecture."""
        print("\n🏗️  Mapping system architecture...")

        architecture = {
            'layers': defaultdict(list),
            'components': defaultdict(dict),
            'entry_points': [],
            'external_dependencies': set()
        }

        for file_path, file_info in self.graph['files'].items():
            if file_info['type'] != '.py':
                continue

            # Identify layers
            if 'deploy/docker' in file_path and 'server.py' in file_path:
                architecture['layers']['API Layer'].append(file_path)
                architecture['entry_points'].append(file_path)
            elif 'async_webcrawler' in file_path or 'adaptive_crawler' in file_path:
                architecture['layers']['Service Layer'].append(file_path)
            elif 'models.py' in file_path or 'types.py' in file_path:
                architecture['layers']['Domain Layer'].append(file_path)
            elif 'database' in file_path or 'cache' in file_path:
                architecture['layers']['Data Layer'].append(file_path)
            elif 'utils' in file_path or 'config' in file_path:
                architecture['layers']['Utility Layer'].append(file_path)

            # Collect external dependencies
            for dep in file_info.get('dependencies', []):
                if not dep.startswith('crawl4ai') and '/' not in dep and '.' in dep:
                    architecture['external_dependencies'].add(dep)

        architecture['external_dependencies'] = sorted(architecture['external_dependencies'])

        print(f"✅ Mapped {len(architecture['layers'])} architectural layers")
        return architecture

    def compute_priority_groups(self):
        """Compute priority groups for migration based on dependencies."""
        print("\n📊 Computing migration priority groups...")

        # Strategy: Files with fewer dependencies and more dependents should be migrated first
        for file_path, file_info in self.graph['files'].items():
            if file_info['type'] != '.py':
                continue

            dep_count = len(file_info.get('dependencies', []))
            dependent_count = len(file_info.get('dependents', []))

            # Compute priority score (higher = more important)
            # More dependents = higher priority (more things depend on it)
            # Fewer dependencies = higher priority (easier to migrate)
            priority_score = (dependent_count * 2) - dep_count

            # Categorize
            if priority_score >= 10:
                self.priority_groups['P0 - Critical Foundation'].append({
                    'file': file_path,
                    'score': priority_score,
                    'dependents': dependent_count,
                    'dependencies': dep_count
                })
            elif priority_score >= 5:
                self.priority_groups['P1 - High Priority'].append({
                    'file': file_path,
                    'score': priority_score,
                    'dependents': dependent_count,
                    'dependencies': dep_count
                })
            elif priority_score >= 0:
                self.priority_groups['P2 - Medium Priority'].append({
                    'file': file_path,
                    'score': priority_score,
                    'dependents': dependent_count,
                    'dependencies': dep_count
                })
            else:
                self.priority_groups['P3 - Low Priority'].append({
                    'file': file_path,
                    'score': priority_score,
                    'dependents': dependent_count,
                    'dependencies': dep_count
                })

        # Sort each group by score
        for group in self.priority_groups.values():
            group.sort(key=lambda x: x['score'], reverse=True)

        total = sum(len(g) for g in self.priority_groups.values())
        print(f"✅ Computed priority groups for {total} Python files")

    def identify_db_schema_candidates(self):
        """Identify potential database schema elements from code."""
        print("\n💾 Identifying database schema candidates...")

        for file_path, file_info in self.graph['files'].items():
            # Look for database-related files
            if 'database' in file_path.lower() or 'models.py' in file_path:
                for cls in file_info.get('classes', []):
                    # Pydantic models or SQLAlchemy models
                    bases = cls.get('bases', [])
                    if any('BaseModel' in b or 'Model' in b or 'Base' in b for b in bases):
                        self.db_candidates.append({
                            'file': file_path,
                            'class': cls['name'],
                            'bases': bases,
                            'type': 'ORM Model' if 'Model' in str(bases) else 'Data Model'
                        })

            # Look for SQL files
            elif file_info['type'] == '.sql':
                for identifier in file_info.get('identifiers', []):
                    if identifier.get('type') == 'table':
                        self.db_candidates.append({
                            'file': file_path,
                            'table': identifier['name'],
                            'type': 'SQL Table'
                        })

        print(f"✅ Identified {len(self.db_candidates)} database schema candidates")

    def generate_markdown_index(self) -> str:
        """Generate the semantic index in Markdown format."""
        print("\n📝 Generating semantic index...")

        md = []

        # Header
        md.append("# Crawl4AI - Semantic Index")
        md.append("")
        md.append("**Generated:** Auto-generated from dependency graph and IR files")
        md.append("")
        md.append("This index provides a semantic overview of the repository for migration planning.")
        md.append("")
        md.append("---")
        md.append("")

        # Table of Contents
        md.append("## Table of Contents")
        md.append("")
        md.append("1. [Repository Summary](#repository-summary)")
        md.append("2. [Domain Clusters](#domain-clusters)")
        md.append("3. [System Architecture](#system-architecture)")
        md.append("4. [Dependency Cycles](#dependency-cycles)")
        md.append("5. [Migration Priority Groups](#migration-priority-groups)")
        md.append("6. [Database Schema Candidates](#database-schema-candidates)")
        md.append("7. [File Index](#file-index)")
        md.append("8. [Migration Groupings](#migration-groupings)")
        md.append("")
        md.append("---")
        md.append("")

        # 1. Repository Summary
        md.append("## Repository Summary")
        md.append("")
        stats = self.graph.get('metadata', {}).get('statistics', {})
        md.append(f"- **Total Files:** {len(self.graph['files'])}")
        md.append(f"- **Python Files:** {self.graph['metadata'].get('file_types', {}).get('.py', 0)}")
        md.append(f"- **Total Imports:** {stats.get('total_imports', 0):,}")
        md.append(f"- **Total Classes:** {stats.get('total_classes', 0):,}")
        md.append(f"- **Total Functions:** {stats.get('total_functions', 0):,}")
        md.append(f"- **IR Files Generated:** {len(self.ir_files)}")
        md.append("")

        # 2. Domain Clusters
        md.append("---")
        md.append("")
        md.append("## Domain Clusters")
        md.append("")
        md.append("Files grouped by domain/functional area:")
        md.append("")

        for cluster_name, files in sorted(self.clusters.items()):
            md.append(f"### {cluster_name}")
            md.append(f"**Files:** {len(files)}")
            md.append("")
            for file in sorted(files)[:10]:
                md.append(f"- `{file}`")
            if len(files) > 10:
                md.append(f"- ... and {len(files) - 10} more files")
            md.append("")

        # 3. System Architecture
        md.append("---")
        md.append("")
        md.append("## System Architecture")
        md.append("")

        architecture = self.map_system_architecture()

        md.append("### Architectural Layers")
        md.append("")
        for layer_name, files in sorted(architecture['layers'].items()):
            md.append(f"**{layer_name}** ({len(files)} files)")
            md.append("")
            for file in sorted(files)[:5]:
                md.append(f"- `{file}`")
            if len(files) > 5:
                md.append(f"- ... and {len(files) - 5} more")
            md.append("")

        md.append("### Entry Points")
        md.append("")
        for entry in architecture['entry_points']:
            md.append(f"- `{entry}`")
        md.append("")

        md.append("### External Dependencies")
        md.append("")
        md.append(f"**Total:** {len(architecture['external_dependencies'])} unique packages")
        md.append("")
        for dep in sorted(architecture['external_dependencies'])[:20]:
            md.append(f"- {dep}")
        if len(architecture['external_dependencies']) > 20:
            md.append(f"- ... and {len(architecture['external_dependencies']) - 20} more")
        md.append("")

        # 4. Dependency Cycles
        md.append("---")
        md.append("")
        md.append("## Dependency Cycles")
        md.append("")

        if self.cycles:
            md.append(f"⚠️ **Found {len(self.cycles)} circular dependencies**")
            md.append("")
            md.append("These should be refactored before migration:")
            md.append("")
            for i, cycle in enumerate(self.cycles[:5], 1):
                md.append(f"### Cycle {i}")
                md.append("")
                for node in cycle:
                    md.append(f"- `{node}`")
                md.append("")
            if len(self.cycles) > 5:
                md.append(f"*... and {len(self.cycles) - 5} more cycles*")
                md.append("")
        else:
            md.append("✅ **No circular dependencies detected**")
            md.append("")

        # 5. Migration Priority Groups
        md.append("---")
        md.append("")
        md.append("## Migration Priority Groups")
        md.append("")
        md.append("Files prioritized by dependency relationships:")
        md.append("")
        md.append("**Priority Score Formula:** `(dependents × 2) - dependencies`")
        md.append("")
        md.append("Higher score = More files depend on it + Fewer dependencies = Migrate first")
        md.append("")

        for group_name in ['P0 - Critical Foundation', 'P1 - High Priority',
                          'P2 - Medium Priority', 'P3 - Low Priority']:
            if group_name in self.priority_groups:
                files = self.priority_groups[group_name]
                md.append(f"### {group_name}")
                md.append(f"**Count:** {len(files)} files")
                md.append("")

                if files:
                    md.append("| File | Score | Dependents | Dependencies |")
                    md.append("|------|-------|------------|--------------|")
                    for item in files[:10]:
                        file_name = Path(item['file']).name
                        md.append(f"| `{file_name}` | {item['score']} | {item['dependents']} | {item['dependencies']} |")
                    if len(files) > 10:
                        md.append(f"| *... and {len(files) - 10} more* | | | |")
                    md.append("")

        # 6. Database Schema Candidates
        md.append("---")
        md.append("")
        md.append("## Database Schema Candidates")
        md.append("")

        if self.db_candidates:
            md.append(f"**Total:** {len(self.db_candidates)} schema elements identified")
            md.append("")

            # Group by type
            by_type = defaultdict(list)
            for candidate in self.db_candidates:
                by_type[candidate['type']].append(candidate)

            for schema_type, items in sorted(by_type.items()):
                md.append(f"### {schema_type}")
                md.append("")
                for item in sorted(items, key=lambda x: x.get('class', x.get('table', '')))[:15]:
                    if 'class' in item:
                        md.append(f"- `{item['class']}` (in {item['file']})")
                    elif 'table' in item:
                        md.append(f"- `{item['table']}` (in {item['file']})")
                if len(items) > 15:
                    md.append(f"- ... and {len(items) - 15} more")
                md.append("")
        else:
            md.append("*No database schema candidates identified*")
            md.append("")

        # 7. File Index
        md.append("---")
        md.append("")
        md.append("## File Index")
        md.append("")
        md.append("Top files by importance (based on dependents):")
        md.append("")

        # Sort Python files by dependent count
        py_files = [(path, info) for path, info in self.graph['files'].items()
                    if info['type'] == '.py']
        py_files.sort(key=lambda x: len(x[1].get('dependents', [])), reverse=True)

        md.append("| File | Type | Classes | Functions | Dependents |")
        md.append("|------|------|---------|-----------|-----------|")
        for file_path, file_info in py_files[:30]:
            file_name = file_path.split('/')[-1] if '/' in file_path else file_path
            classes = len(file_info.get('classes', []))
            functions = len(file_info.get('functions', []))
            dependents = len(file_info.get('dependents', []))
            md.append(f"| `{file_name}` | {file_info['type']} | {classes} | {functions} | {dependents} |")
        md.append("")

        # 8. Migration Groupings
        md.append("---")
        md.append("")
        md.append("## Migration Groupings")
        md.append("")
        md.append("Suggested migration order by domain cluster:")
        md.append("")

        migration_order = [
            ('Core Models', 'Foundation types and data structures'),
            ('Shared Components', 'Reusable utilities and helpers'),
            ('Infrastructure', 'Database, logging, async primitives'),
            ('Browser Management', 'Browser automation and lifecycle'),
            ('Content Processing', 'Extraction, filtering, scraping strategies'),
            ('Crawling Engine', 'Core crawling logic'),
            ('API Server', 'REST API and job queue'),
            ('Chrome Extension', 'Browser extension'),
            ('Frontend', 'Web dashboards'),
        ]

        for i, (cluster, description) in enumerate(migration_order, 1):
            if cluster in self.clusters:
                files = self.clusters[cluster]
                md.append(f"### Phase {i}: {cluster}")
                md.append(f"*{description}*")
                md.append("")
                md.append(f"**Files:** {len(files)}")
                md.append("")
                md.append(f"**Rationale:** {self.get_migration_rationale(cluster)}")
                md.append("")

        md.append("---")
        md.append("")
        md.append("*End of Semantic Index*")

        return '\n'.join(md)

    def get_migration_rationale(self, cluster: str) -> str:
        """Get migration rationale for a cluster."""
        rationales = {
            'Core Models': 'These are foundational types used throughout the codebase. Migrate first to ensure type safety.',
            'Shared Components': 'Reusable utilities with minimal dependencies. Good candidates for early migration.',
            'Infrastructure': 'Core infrastructure services that other modules depend on.',
            'Browser Management': 'Browser automation layer - relatively independent.',
            'Content Processing': 'Business logic for content extraction - depends on models.',
            'Crawling Engine': 'Core crawling logic - depends on browser management and content processing.',
            'API Server': 'High-level API layer - depends on crawling engine.',
            'Chrome Extension': 'Standalone browser extension - can be migrated independently.',
            'Frontend': 'Web UIs - can be modernized independently with new frameworks.',
        }
        return rationales.get(cluster, 'See dependency graph for details.')

    def generate(self):
        """Main generation process."""
        self.load_data()
        self.detect_domain_clusters()
        self.detect_dependency_cycles()
        self.compute_priority_groups()
        self.identify_db_schema_candidates()

        markdown = self.generate_markdown_index()

        output_path = self.prompt_dir / 'semantic-index.md'
        print(f"\n💾 Writing semantic index to: {output_path}")
        output_path.write_text(markdown, encoding='utf-8')

        file_size = output_path.stat().st_size
        print(f"✅ Written {file_size:,} bytes")

    def print_summary(self):
        """Print summary statistics."""
        print("\n" + "="*70)
        print("📈 SEMANTIC INDEX SUMMARY")
        print("="*70)
        print(f"Domain clusters: {len(self.clusters)}")
        print(f"Dependency cycles: {len(self.cycles)}")
        print(f"Priority groups: {len(self.priority_groups)}")
        print(f"DB schema candidates: {len(self.db_candidates)}")
        print(f"Total Python files: {self.graph['metadata'].get('file_types', {}).get('.py', 0)}")
        print("="*70)


def main():
    """Main entry point."""
    script_path = Path(__file__).resolve()
    repo_root = script_path.parent.parent

    print("🚀 Crawl4AI Semantic Index Generator")
    print(f"📂 Repository: {repo_root}")
    print(f"🎯 Output: .prompt/semantic-index.md")
    print()

    generator = SemanticIndexGenerator(str(repo_root))
    generator.generate()
    generator.print_summary()

    print("\n✨ Done!")


if __name__ == '__main__':
    import sys
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
