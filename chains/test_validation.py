#!/usr/bin/env python3
"""
Chain Validation Test Suite
Author: Victor Ibhafidon

Comprehensive test suite for validating attack chain logic and prerequisites.

WHAT IT DOES:
- Tests basic chain validation (valid chains pass)
- Tests missing prerequisite detection
- Tests fuzzy matching for similar prerequisites
- Tests missing outcome detection
- Tests empty chain validation

HOW IT CONNECTS TO THE FRAMEWORK:
- Tests the validation logic in chain_analyzer.py
- Ensures chains are logically sound before use
- Validates that prerequisite matching works correctly
- Used during development to verify validation improvements

USAGE:
    python chains/test_validation.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from chain_analyzer import (
    ChainAnalyzer, ChainStep, VulnerabilityType, ImpactLevel
)


def test_basic_validation():
    """Test basic chain validation"""
    print("=" * 80)
    print("TEST 1: Basic Valid Chain")
    print("=" * 80)
    
    analyzer = ChainAnalyzer()
    chain = analyzer.create_chain(
        title="Test Chain",
        description="A valid test chain",
        impact=ImpactLevel.HIGH
    )
    
    step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile", outcome="XSS stored")
    step2 = ChainStep(2, VulnerabilityType.IDOR, "IDOR access", 
                     prerequisites=["XSS stored"], outcome="Data accessed")
    
    chain.add_step(step1)
    chain.add_step(step2)
    
    is_valid, issues = chain.validate_chain()
    print(f"Valid: {is_valid}")
    if issues:
        print("Issues/Suggestions:")
        for issue in issues:
            print(f"  {issue}")
    print()


def test_missing_prerequisite():
    """Test chain with missing prerequisite"""
    print("=" * 80)
    print("TEST 2: Missing Prerequisite")
    print("=" * 80)
    
    analyzer = ChainAnalyzer()
    chain = analyzer.create_chain(
        title="Invalid Chain",
        description="Chain with missing prerequisite",
        impact=ImpactLevel.HIGH
    )
    
    step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile", outcome="XSS executed")
    step2 = ChainStep(2, VulnerabilityType.IDOR, "IDOR access", 
                     prerequisites=["Session stolen"], outcome="Data accessed")
    
    chain.add_step(step1)
    chain.add_step(step2)
    
    is_valid, issues = chain.validate_chain()
    print(f"Valid: {is_valid}")
    if issues:
        print("Issues/Suggestions:")
        for issue in issues:
            print(f"  {issue}")
    print()


def test_fuzzy_matching():
    """Test fuzzy matching for similar prerequisites"""
    print("=" * 80)
    print("TEST 3: Fuzzy Matching (Similar Prerequisites)")
    print("=" * 80)
    
    analyzer = ChainAnalyzer()
    chain = analyzer.create_chain(
        title="Fuzzy Match Test",
        description="Testing fuzzy prerequisite matching",
        impact=ImpactLevel.HIGH
    )
    
    step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile", 
                     outcome="XSS payload stored in profile")
    step2 = ChainStep(2, VulnerabilityType.IDOR, "IDOR access", 
                     prerequisites=["XSS stored"], outcome="Data accessed")
    
    chain.add_step(step1)
    chain.add_step(step2)
    
    is_valid, issues = chain.validate_chain()
    print(f"Valid: {is_valid}")
    if issues:
        print("Issues/Suggestions:")
        for issue in issues:
            print(f"  {issue}")
    print()


def test_missing_outcome():
    """Test chain with missing outcome"""
    print("=" * 80)
    print("TEST 4: Missing Outcome")
    print("=" * 80)
    
    analyzer = ChainAnalyzer()
    chain = analyzer.create_chain(
        title="Missing Outcome Test",
        description="Testing missing outcome detection",
        impact=ImpactLevel.HIGH
    )
    
    step1 = ChainStep(1, VulnerabilityType.XSS, "XSS in profile")  # No outcome
    step2 = ChainStep(2, VulnerabilityType.IDOR, "IDOR access", 
                     prerequisites=["XSS result"], outcome="Data accessed")
    
    chain.add_step(step1)
    chain.add_step(step2)
    
    is_valid, issues = chain.validate_chain()
    print(f"Valid: {is_valid}")
    if issues:
        print("Issues/Suggestions:")
        for issue in issues:
            print(f"  {issue}")
    print()


def test_empty_chain():
    """Test empty chain"""
    print("=" * 80)
    print("TEST 5: Empty Chain")
    print("=" * 80)
    
    analyzer = ChainAnalyzer()
    chain = analyzer.create_chain(
        title="Empty Chain",
        description="Testing empty chain validation",
        impact=ImpactLevel.HIGH
    )
    
    is_valid, issues = chain.validate_chain()
    print(f"Valid: {is_valid}")
    if issues:
        print("Issues/Suggestions:")
        for issue in issues:
            print(f"  {issue}")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("CHAIN VALIDATION TEST SUITE")
    print("=" * 80)
    print()
    
    test_basic_validation()
    test_missing_prerequisite()
    test_fuzzy_matching()
    test_missing_outcome()
    test_empty_chain()
    
    print("=" * 80)
    print("All tests completed!")
    print("=" * 80)


