#!/usr/bin/env python3
"""
Chain Dependency Analyzer
Author: Victor Ibhafidon

WHAT IT DOES:
- Maps dependencies between attack chains
- Visualizes chain relationships
- Identifies critical paths
- Suggests optimizations
- Finds chain clusters and patterns

HOW IT CONNECTS TO THE FRAMEWORK:
- Uses chain_analyzer.py for chain data
- Integrates with visualizer.py for graph visualization
- Helps identify related attack scenarios
- Supports chain optimization and planning

USAGE:
    from chains.dependency_analyzer import DependencyAnalyzer
    
    analyzer = DependencyAnalyzer()
    dependencies = analyzer.analyze_dependencies(chains)
    graph = analyzer.visualize_dependencies(dependencies)
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
    """Graph of chain dependencies"""
    chains: List[AttackChain]
    dependencies: List[ChainDependency]
    clusters: List[List[str]] = field(default_factory=list)
    critical_paths: List[List[str]] = field(default_factory=list)


class DependencyAnalyzer:
    """Analyzes dependencies between attack chains"""
    
    def analyze_dependencies(self, chains: List[AttackChain]) -> DependencyGraph:
        """Analyze dependencies between chains"""
        dependencies = []
        
        # Find all types of dependencies
        for i, chain1 in enumerate(chains):
            for j, chain2 in enumerate(chains):
                if i >= j:
                    continue
                
                # Check for prerequisite dependencies
                prereq_dep = self._check_prerequisite_dependency(chain1, chain2)
                if prereq_dep:
                    dependencies.append(prereq_dep)
                
                # Check for similarity dependencies
                similar_dep = self._check_similarity_dependency(chain1, chain2)
                if similar_dep:
                    dependencies.append(similar_dep)
                
                # Check for sequential dependencies
                seq_dep = self._check_sequential_dependency(chain1, chain2)
                if seq_dep:
                    dependencies.append(seq_dep)
        
        # Find clusters
        clusters = self._find_clusters(chains, dependencies)
        
        # Find critical paths
        critical_paths = self._find_critical_paths(chains, dependencies)
        
        return DependencyGraph(
            chains=chains,
            dependencies=dependencies,
            clusters=clusters,
            critical_paths=critical_paths
        )
    
    def _check_prerequisite_dependency(
        self, 
        chain1: AttackChain, 
        chain2: AttackChain
    ) -> Optional[ChainDependency]:
        """Check if chain1 is a prerequisite for chain2"""
        # Check if chain1's final outcome is a prerequisite for chain2
        if not chain1.steps or not chain2.steps:
            return None
        
        chain1_outcome = chain1.steps[-1].outcome
        if not chain1_outcome:
            return None
        
        # Check if chain2 has chain1's outcome as a prerequisite
        for step in chain2.steps:
            if chain1_outcome in step.prerequisites:
                return ChainDependency(
                    source_chain=chain1.title,
                    target_chain=chain2.title,
                    dependency_type="prerequisite",
                    strength=0.9,
                    reason=f"Chain '{chain2.title}' requires outcome from '{chain1.title}'"
                )
        
        return None
    
    def _check_similarity_dependency(
        self, 
        chain1: AttackChain, 
        chain2: AttackChain
    ) -> Optional[ChainDependency]:
        """Check if chains are similar (related)"""
        # Count common vulnerabilities
        vulns1 = {step.vulnerability_type for step in chain1.steps}
        vulns2 = {step.vulnerability_type for step in chain2.steps}
        common_vulns = vulns1 & vulns2
        
        if len(common_vulns) >= 2:  # At least 2 common vulnerabilities
            similarity = len(common_vulns) / max(len(vulns1), len(vulns2))
            if similarity > 0.5:  # 50% similarity threshold
                return ChainDependency(
                    source_chain=chain1.title,
                    target_chain=chain2.title,
                    dependency_type="similar",
                    strength=similarity,
                    reason=f"Share {len(common_vulns)} common vulnerabilities"
                )
        
        # Check for common tags
        common_tags = chain1.tags & chain2.tags
        if len(common_tags) >= 2:
            return ChainDependency(
                source_chain=chain1.title,
                target_chain=chain2.title,
                dependency_type="related",
                strength=0.6,
                reason=f"Share tags: {', '.join(common_tags)}"
            )
        
        return None
    
    def _check_sequential_dependency(
        self, 
        chain1: AttackChain, 
        chain2: AttackChain
    ) -> Optional[ChainDependency]:
        """Check if chain2 logically follows chain1"""
        # Check if chain1's impact enables chain2
        if chain1.impact.value == "Critical" and chain2.impact.value in ["High", "Medium"]:
            # Check if chain2 builds on chain1's outcome
            if chain1.steps and chain2.steps:
                chain1_final = chain1.steps[-1]
                chain2_first = chain2.steps[0]
                
                # Check if chain2's first step could logically follow chain1
                if chain1_final.vulnerability_type == VulnerabilityType.PRIV_ESCALATION:
                    if chain2_first.vulnerability_type in [
                        VulnerabilityType.IDOR,
                        VulnerabilityType.BUSINESS_LOGIC,
                        VulnerabilityType.AUTH_BYPASS
                    ]:
                        return ChainDependency(
                            source_chain=chain1.title,
                            target_chain=chain2.title,
                            dependency_type="follows",
                            strength=0.7,
                            reason=f"'{chain2.title}' can follow privilege escalation from '{chain1.title}'"
                        )
        
        return None
    
    def _find_clusters(
        self, 
        chains: List[AttackChain], 
        dependencies: List[ChainDependency]
    ) -> List[List[str]]:
        """Find clusters of related chains"""
        # Build adjacency list
        graph = defaultdict(set)
        for dep in dependencies:
            graph[dep.source_chain].add(dep.target_chain)
            graph[dep.target_chain].add(dep.source_chain)
        
        # Find connected components
        visited = set()
        clusters = []
        
        for chain in chains:
            if chain.title in visited:
                continue
            
            # BFS to find connected component
            cluster = []
            queue = [chain.title]
            visited.add(chain.title)
            
            while queue:
                current = queue.pop(0)
                cluster.append(current)
                
                for neighbor in graph.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            if len(cluster) > 1:  # Only clusters with 2+ chains
                clusters.append(cluster)
        
        return clusters
    
    def _find_critical_paths(
        self, 
        chains: List[AttackChain], 
        dependencies: List[ChainDependency]
    ) -> List[List[str]]:
        """Find critical paths through chains"""
        # Build directed graph
        graph = defaultdict(list)
        for dep in dependencies:
            if dep.dependency_type in ["prerequisite", "follows"]:
                graph[dep.source_chain].append(dep.target_chain)
        
        # Find longest paths (critical paths)
        critical_paths = []
        
        def dfs(chain_title: str, path: List[str], visited: Set[str]):
            if chain_title in visited:
                return
            
            visited.add(chain_title)
            path.append(chain_title)
            
            if not graph[chain_title]:  # End of path
                if len(path) > 1:
                    critical_paths.append(path.copy())
            else:
                for next_chain in graph[chain_title]:
                    dfs(next_chain, path, visited)
            
            path.pop()
            visited.remove(chain_title)
        
        # Start DFS from each chain
        for chain in chains:
            dfs(chain.title, [], set())
        
        # Sort by length (longest first)
        critical_paths.sort(key=len, reverse=True)
        
        return critical_paths[:5]  # Return top 5 critical paths
    
    def visualize_dependencies(self, graph: DependencyGraph) -> str:
        """Generate Mermaid diagram for dependencies"""
        mermaid = ["graph TD"]
        
        # Add nodes
        for chain in graph.chains:
            chain_id = chain.title.replace(" ", "_").replace("-", "_")
            impact_color = {
                "Critical": "red",
                "High": "orange",
                "Medium": "yellow",
                "Low": "green"
            }.get(chain.impact.value, "gray")
            
            mermaid.append(f'    {chain_id}["{chain.title}"]')
        
        # Add edges
        for dep in graph.dependencies:
            source_id = dep.source_chain.replace(" ", "_").replace("-", "_")
            target_id = dep.target_chain.replace(" ", "_").replace("-", "_")
            
            edge_style = {
                "prerequisite": "-->",
                "follows": "-->",
                "similar": "-.-",
                "related": "-.-"
            }.get(dep.dependency_type, "-->")
            
            mermaid.append(f'    {source_id}{edge_style}{target_id}')
        
        return "\n".join(mermaid)
    
    def generate_report(self, graph: DependencyGraph) -> str:
        """Generate dependency analysis report"""
        report = []
        report.append("=" * 80)
        report.append("CHAIN DEPENDENCY ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        report.append(f"Total Chains: {len(graph.chains)}")
        report.append(f"Total Dependencies: {len(graph.dependencies)}")
        report.append(f"Clusters Found: {len(graph.clusters)}")
        report.append(f"Critical Paths: {len(graph.critical_paths)}")
        report.append("")
        
        # Dependencies by type
        by_type = defaultdict(list)
        for dep in graph.dependencies:
            by_type[dep.dependency_type].append(dep)
        
        report.append("-" * 80)
        report.append("DEPENDENCIES BY TYPE")
        report.append("-" * 80)
        for dep_type, deps in by_type.items():
            report.append(f"\n{dep_type.upper()}: {len(deps)}")
            for dep in deps[:5]:  # Show first 5
                report.append(f"  {dep.source_chain} -> {dep.target_chain}")
                report.append(f"    Reason: {dep.reason}")
                report.append(f"    Strength: {dep.strength:.2f}")
        
        # Clusters
        if graph.clusters:
            report.append("")
            report.append("-" * 80)
            report.append("CHAIN CLUSTERS")
            report.append("-" * 80)
            for i, cluster in enumerate(graph.clusters, 1):
                report.append(f"\nCluster {i} ({len(cluster)} chains):")
                for chain_title in cluster:
                    report.append(f"  - {chain_title}")
        
        # Critical paths
        if graph.critical_paths:
            report.append("")
            report.append("-" * 80)
            report.append("CRITICAL PATHS")
            report.append("-" * 80)
            for i, path in enumerate(graph.critical_paths, 1):
                report.append(f"\nPath {i} ({len(path)} chains):")
                report.append(" -> ".join(path))
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def suggest_optimizations(self, graph: DependencyGraph) -> List[str]:
        """Suggest optimizations based on dependencies"""
        suggestions = []
        
        # Check for redundant chains
        similar_chains = [
            dep for dep in graph.dependencies 
            if dep.dependency_type == "similar" and dep.strength > 0.8
        ]
        if similar_chains:
            suggestions.append(
                f"Found {len(similar_chains)} highly similar chains. "
                "Consider consolidating or documenting differences."
            )
        
        # Check for long critical paths
        if graph.critical_paths:
            longest = max(graph.critical_paths, key=len)
            if len(longest) > 3:
                suggestions.append(
                    f"Long critical path found ({len(longest)} chains). "
                    "Consider breaking into smaller, testable components."
                )
        
        # Check for isolated chains
        connected_chains = set()
        for dep in graph.dependencies:
            connected_chains.add(dep.source_chain)
            connected_chains.add(dep.target_chain)
        
        isolated = [c.title for c in graph.chains if c.title not in connected_chains]
        if isolated:
            suggestions.append(
                f"Found {len(isolated)} isolated chains. "
                "Consider linking them to other chains or documenting why they're standalone."
            )
        
        return suggestions


if __name__ == "__main__":
    # Example usage
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    
    from chains.chain_analyzer import ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
    
    # Create example chains
    analyzer = ChainAnalyzer()
    
    chain1 = analyzer.create_chain(
        "XSS to Session Theft",
        "XSS leading to session hijacking",
        ImpactLevel.HIGH
    )
    step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile", outcome="XSS stored")
    step2 = ChainStep(2, VulnerabilityType.SESSION_HIJACKING, "Session stolen", 
                     prerequisites=["XSS stored"], outcome="Session token obtained")
    chain1.add_step(step1)
    chain1.add_step(step2)
    
    chain2 = analyzer.create_chain(
        "Session Token to Admin Access",
        "Using stolen session for admin access",
        ImpactLevel.CRITICAL
    )
    step3 = ChainStep(1, VulnerabilityType.AUTH_BYPASS, "Use session token",
                     prerequisites=["Session token obtained"], outcome="Admin access")
    chain2.add_step(step3)
    
    # Analyze dependencies
    dep_analyzer = DependencyAnalyzer()
    graph = dep_analyzer.analyze_dependencies([chain1, chain2])
    
    print(dep_analyzer.generate_report(graph))
    print("\n" + "=" * 80)
    print("DEPENDENCY DIAGRAM")
    print("=" * 80)
    print(dep_analyzer.visualize_dependencies(graph))
    print("\n" + "=" * 80)
    print("OPTIMIZATION SUGGESTIONS")
    print("=" * 80)
    for suggestion in dep_analyzer.suggest_optimizations(graph):
        print(f"- {suggestion}")

