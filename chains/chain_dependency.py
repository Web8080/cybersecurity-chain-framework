#!/usr/bin/env python3
"""
Chain Dependency Analysis Module
Author: Victor Ibhafidon

WHAT IT DOES:
- Maps dependencies between attack chains
- Visualizes chain relationships
- Identifies critical paths
- Suggests optimizations
- Creates dependency graphs

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py for chain data
- Integrates with visualizer.py for graph visualization
- Helps identify related chains and attack patterns
- Supports chain optimization and analysis

USAGE:
    from chains.chain_dependency import ChainDependencyAnalyzer
    
    analyzer = ChainDependencyAnalyzer()
    dependencies = analyzer.analyze_dependencies(chains)
    graph = analyzer.create_dependency_graph(dependencies)
    critical_paths = analyzer.find_critical_paths(dependencies)
"""

import sys
import os
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

# Add chains directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chains.chain_analyzer import AttackChain, ChainStep, VulnerabilityType


@dataclass
class ChainDependency:
    """Represents a dependency between two chains"""
    source_chain: str
    target_chain: str
    dependency_type: str  # "prerequisite", "similar", "follows", "related"
    strength: float  # 0.0 to 1.0
    reason: str


@dataclass
class DependencyGraph:
    """Graph structure for chain dependencies"""
    nodes: Set[str] = field(default_factory=set)
    edges: List[Tuple[str, str, float]] = field(default_factory=list)
    node_data: Dict[str, dict] = field(default_factory=dict)


class ChainDependencyAnalyzer:
    """Analyzes dependencies between attack chains"""
    
    def __init__(self):
        """Initialize the dependency analyzer"""
        self.chains: List[AttackChain] = []
    
    def analyze_dependencies(
        self, 
        chains: List[AttackChain]
    ) -> List[ChainDependency]:
        """
        Analyze dependencies between chains
        
        Args:
            chains: List of attack chains to analyze
        
        Returns:
            List of chain dependencies
        """
        self.chains = chains
        dependencies = []
        
        for i, chain1 in enumerate(chains):
            for j, chain2 in enumerate(chains):
                if i >= j:
                    continue
                
                # Check for various dependency types
                deps = self._find_dependencies(chain1, chain2)
                dependencies.extend(deps)
        
        return dependencies
    
    def _find_dependencies(
        self, 
        chain1: AttackChain, 
        chain2: AttackChain
    ) -> List[ChainDependency]:
        """Find dependencies between two chains"""
        dependencies = []
        
        # Check if chain2's prerequisites match chain1's outcomes
        for step2 in chain2.steps:
            if step2.prerequisites:
                for prereq in step2.prerequisites:
                    # Check if any step in chain1 produces this outcome
                    for step1 in chain1.steps:
                        if step1.outcome and prereq.lower() in step1.outcome.lower():
                            dependencies.append(ChainDependency(
                                source_chain=chain1.title,
                                target_chain=chain2.title,
                                dependency_type="prerequisite",
                                strength=0.8,
                                reason=f"Chain2 requires '{prereq}' which Chain1 produces"
                            ))
        
        # Check for similar vulnerability sequences
        vulns1 = [step.vulnerability_type for step in chain1.steps]
        vulns2 = [step.vulnerability_type for step in chain2.steps]
        
        if len(vulns1) > 0 and len(vulns2) > 0:
            # Check for common starting vulnerabilities
            if vulns1[0] == vulns2[0]:
                dependencies.append(ChainDependency(
                    source_chain=chain1.title,
                    target_chain=chain2.title,
                    dependency_type="similar",
                    strength=0.6,
                    reason="Both chains start with the same vulnerability type"
                ))
            
            # Check for common ending vulnerabilities
            if vulns1[-1] == vulns2[-1]:
                dependencies.append(ChainDependency(
                    source_chain=chain1.title,
                    target_chain=chain2.title,
                    dependency_type="similar",
                    strength=0.6,
                    reason="Both chains end with the same vulnerability type"
                ))
        
        # Check for shared tags
        shared_tags = chain1.tags & chain2.tags
        if shared_tags:
            dependencies.append(ChainDependency(
                source_chain=chain1.title,
                target_chain=chain2.title,
                dependency_type="related",
                strength=0.4,
                reason=f"Shared tags: {', '.join(shared_tags)}"
            ))
        
        # Check if chains target the same endpoint
        endpoints1 = {step.endpoint for step in chain1.steps if step.endpoint}
        endpoints2 = {step.endpoint for step in chain2.steps if step.endpoint}
        common_endpoints = endpoints1 & endpoints2
        if common_endpoints:
            dependencies.append(ChainDependency(
                source_chain=chain1.title,
                target_chain=chain2.title,
                dependency_type="related",
                strength=0.5,
                reason=f"Target same endpoints: {', '.join(common_endpoints)}"
            ))
        
        return dependencies
    
    def create_dependency_graph(
        self, 
        dependencies: List[ChainDependency]
    ) -> DependencyGraph:
        """
        Create a graph structure from dependencies
        
        Args:
            dependencies: List of chain dependencies
        
        Returns:
            Dependency graph
        """
        graph = DependencyGraph()
        
        for dep in dependencies:
            graph.nodes.add(dep.source_chain)
            graph.nodes.add(dep.target_chain)
            graph.edges.append((dep.source_chain, dep.target_chain, dep.strength))
        
        return graph
    
    def find_critical_paths(
        self, 
        dependencies: List[ChainDependency],
        max_depth: int = 5
    ) -> List[List[str]]:
        """
        Find critical paths through the dependency graph
        
        Args:
            dependencies: List of chain dependencies
            max_depth: Maximum depth to search
        
        Returns:
            List of critical paths (each path is a list of chain titles)
        """
        graph = self.create_dependency_graph(dependencies)
        
        # Build adjacency list
        adj = defaultdict(list)
        for source, target, strength in graph.edges:
            adj[source].append((target, strength))
        
        # Find all paths
        all_paths = []
        
        def dfs(node: str, path: List[str], depth: int):
            if depth > max_depth:
                return
            
            if len(path) > 1:
                all_paths.append(path[:])
            
            for neighbor, strength in adj.get(node, []):
                if neighbor not in path:
                    dfs(neighbor, path + [neighbor], depth + 1)
        
        for node in graph.nodes:
            dfs(node, [node], 0)
        
        # Sort by path length and strength
        all_paths.sort(key=lambda p: (len(p), -sum(
            strength for _, target, strength in graph.edges
            if any((p[i] == source and p[i+1] == target) 
                   for i in range(len(p)-1))
        )), reverse=True)
        
        return all_paths[:10]  # Return top 10 paths
    
    def suggest_optimizations(
        self, 
        dependencies: List[ChainDependency]
    ) -> List[str]:
        """
        Suggest optimizations based on dependencies
        
        Args:
            dependencies: List of chain dependencies
        
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        # Group by dependency type
        by_type = defaultdict(list)
        for dep in dependencies:
            by_type[dep.dependency_type].append(dep)
        
        # Suggest combining chains with prerequisite dependencies
        prerequisite_deps = by_type.get("prerequisite", [])
        if len(prerequisite_deps) > 0:
            suggestions.append(
                f"Found {len(prerequisite_deps)} prerequisite dependencies. "
                "Consider combining related chains into longer attack scenarios."
            )
        
        # Suggest grouping similar chains
        similar_deps = by_type.get("similar", [])
        if len(similar_deps) > 0:
            suggestions.append(
                f"Found {len(similar_deps)} similar chains. "
                "Consider creating a template or pattern for these common attack vectors."
            )
        
        # Suggest analyzing related chains together
        related_deps = by_type.get("related", [])
        if len(related_deps) > 0:
            suggestions.append(
                f"Found {len(related_deps)} related chains. "
                "These chains may be part of a larger attack campaign."
            )
        
        return suggestions
    
    def generate_dependency_report(
        self, 
        dependencies: List[ChainDependency]
    ) -> str:
        """
        Generate a text report of dependencies
        
        Args:
            dependencies: List of chain dependencies
        
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 80)
        report.append("CHAIN DEPENDENCY ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        if not dependencies:
            report.append("No dependencies found between chains.")
            return "\n".join(report)
        
        # Group by type
        by_type = defaultdict(list)
        for dep in dependencies:
            by_type[dep.dependency_type].append(dep)
        
        report.append(f"Total Dependencies: {len(dependencies)}")
        report.append("")
        
        for dep_type, deps in by_type.items():
            report.append(f"{dep_type.upper()} DEPENDENCIES ({len(deps)}):")
            report.append("-" * 80)
            for dep in deps:
                report.append(f"  {dep.source_chain} → {dep.target_chain}")
                report.append(f"    Strength: {dep.strength:.2f}")
                report.append(f"    Reason: {dep.reason}")
                report.append("")
        
        # Critical paths
        critical_paths = self.find_critical_paths(dependencies)
        if critical_paths:
            report.append("CRITICAL PATHS:")
            report.append("-" * 80)
            for i, path in enumerate(critical_paths[:5], 1):
                report.append(f"  Path {i}: {' → '.join(path)}")
            report.append("")
        
        # Optimizations
        suggestions = self.suggest_optimizations(dependencies)
        if suggestions:
            report.append("OPTIMIZATION SUGGESTIONS:")
            report.append("-" * 80)
            for suggestion in suggestions:
                report.append(f"  • {suggestion}")
            report.append("")
        
        report.append("=" * 80)
        return "\n".join(report)
    
    def export_dependency_graph(
        self, 
        dependencies: List[ChainDependency],
        output_file: str,
        format: str = "mermaid"
    ) -> str:
        """
        Export dependency graph to file
        
        Args:
            dependencies: List of chain dependencies
            output_file: Output file path
            format: Export format ("mermaid" or "dot")
        
        Returns:
            Path to exported file
        """
        graph = self.create_dependency_graph(dependencies)
        
        if format == "mermaid":
            content = self._generate_mermaid_graph(graph, dependencies)
        elif format == "dot":
            content = self._generate_dot_graph(graph, dependencies)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"Dependency graph exported to: {output_file}")
        return output_file
    
    def _generate_mermaid_graph(
        self, 
        graph: DependencyGraph,
        dependencies: List[ChainDependency]
    ) -> str:
        """Generate Mermaid diagram code"""
        lines = ["graph TD"]
        
        # Add nodes
        for node in graph.nodes:
            safe_node = node.replace(' ', '_').replace('-', '_')
            lines.append(f"    {safe_node}[\"{node}\"]")
        
        # Add edges with labels
        for dep in dependencies:
            source = dep.source_chain.replace(' ', '_').replace('-', '_')
            target = dep.target_chain.replace(' ', '_').replace('-', '_')
            label = f"{dep.dependency_type} ({dep.strength:.2f})"
            lines.append(f"    {source} -->|{label}| {target}")
        
        return "\n".join(lines)
    
    def _generate_dot_graph(
        self, 
        graph: DependencyGraph,
        dependencies: List[ChainDependency]
    ) -> str:
        """Generate Graphviz DOT format"""
        lines = ["digraph ChainDependencies {"]
        lines.append("    rankdir=LR;")
        lines.append("    node [shape=box];")
        
        # Add edges
        for dep in dependencies:
            source = f'"{dep.source_chain}"'
            target = f'"{dep.target_chain}"'
            label = f'label="{dep.dependency_type}\\n{dep.strength:.2f}"'
            lines.append(f"    {source} -> {target} [{label}];")
        
        lines.append("}")
        return "\n".join(lines)


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from chains.chain_analyzer import ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
    import glob
    
    # Load existing chains
    analyzer = ChainDependencyAnalyzer()
    chain_analyzer = ChainAnalyzer()
    
    # Load chains from JSON files
    chain_files = glob.glob(
        os.path.join(os.path.dirname(__file__), 'chain_templates', 'exports', '*.json')
    )
    
    chains = []
    for chain_file in chain_files[:5]:  # Limit to 5 for example
        try:
            chain = chain_analyzer.import_chain(chain_file)
            chains.append(chain)
        except:
            pass
    
    if not chains:
        # Create example chains
        chain1 = chain_analyzer.create_chain(
            "XSS to Session Theft",
            "XSS leading to session hijacking",
            ImpactLevel.HIGH
        )
        step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile", outcome="XSS stored")
        chain1.add_step(step1)
        chains.append(chain1)
        
        chain2 = chain_analyzer.create_chain(
            "Session Theft to Admin Access",
            "Using stolen session to gain admin",
            ImpactLevel.CRITICAL
        )
        step2 = ChainStep(2, VulnerabilityType.SESSION_HIJACKING, "Use stolen session", 
                         prerequisites=["XSS stored"], outcome="Admin access")
        chain2.add_step(step2)
        chains.append(chain2)
    
    # Analyze dependencies
    print("=" * 80)
    print("CHAIN DEPENDENCY ANALYSIS")
    print("=" * 80)
    print()
    
    dependencies = analyzer.analyze_dependencies(chains)
    report = analyzer.generate_dependency_report(dependencies)
    print(report)
    
    # Export graph
    output_file = os.path.join(
        os.path.dirname(__file__), '..', 'docs', 'exports', 'dependency_graph.mmd'
    )
    analyzer.export_dependency_graph(dependencies, output_file, format="mermaid")
    print(f"\nDependency graph exported to: {output_file}")

