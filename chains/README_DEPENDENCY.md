# Chain Dependency Analysis

**Author:** Victor Ibhafidon

## Overview

Analyzes relationships and dependencies between attack chains to identify patterns, critical paths, and optimization opportunities.

## Features

- **Dependency Detection**: Identifies prerequisite, similar, and related chains
- **Critical Path Analysis**: Finds important attack sequences
- **Optimization Suggestions**: Recommends chain combinations and patterns
- **Graph Visualization**: Exports dependency graphs in Mermaid and DOT formats

## Usage

```python
from chains.chain_dependency import ChainDependencyAnalyzer
from chains.chain_analyzer import ChainAnalyzer

# Load chains
chain_analyzer = ChainAnalyzer()
chains = chain_analyzer.chains  # Or load from JSON files

# Analyze dependencies
dependency_analyzer = ChainDependencyAnalyzer()
dependencies = dependency_analyzer.analyze_dependencies(chains)

# Generate report
report = dependency_analyzer.generate_dependency_report(dependencies)
print(report)

# Find critical paths
critical_paths = dependency_analyzer.find_critical_paths(dependencies)

# Export graph
dependency_analyzer.export_dependency_graph(
    dependencies, 
    "dependency_graph.mmd", 
    format="mermaid"
)
```

## Dependency Types

1. **Prerequisite**: Chain B requires an outcome from Chain A
2. **Similar**: Chains share vulnerability sequences or patterns
3. **Related**: Chains share tags, endpoints, or context

## Output Formats

- **Mermaid**: For web-based visualization
- **DOT**: For Graphviz rendering

