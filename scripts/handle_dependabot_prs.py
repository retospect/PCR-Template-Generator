#!/usr/bin/env python3
"""
Handle Dependabot Pull Requests

This script helps manage Dependabot PRs by categorizing them and providing
recommendations for safe updates.

Usage:
    python scripts/handle_dependabot_prs.py
"""

import json
import subprocess
import sys
from pathlib import Path
import re


def run_command(cmd, capture_output=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def get_dependabot_prs():
    """Get all open Dependabot PRs."""
    success, stdout, stderr = run_command(
        "gh pr list --state open --author app/dependabot --json number,title,headRefName,createdAt,url"
    )
    
    if not success:
        print(f"❌ Failed to get PRs: {stderr}")
        return []
    
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        print("❌ Failed to parse PR data")
        return []


def parse_dependency_update(title):
    """Parse dependency update information from PR title."""
    # Pattern: "deps(deps-dev): bump package from x.y.z to a.b.c"
    # Pattern: "ci(deps): bump action/name from x to y"
    
    patterns = [
        r"deps\(deps(?:-dev)?\): bump (.+) from (.+) to (.+)",
        r"ci\(deps\): bump (.+) from (.+) to (.+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, title)
        if match:
            package = match.group(1)
            old_version = match.group(2)
            new_version = match.group(3)
            
            # Determine type
            if "ci(deps)" in title:
                dep_type = "github_actions"
            elif "deps-dev" in title:
                dep_type = "dev_dependency"
            else:
                dep_type = "main_dependency"
            
            return {
                'package': package,
                'old_version': old_version,
                'new_version': new_version,
                'type': dep_type
            }
    
    return None


def check_version_compatibility(package, new_version, dep_type):
    """Check if the new version is compatible with our constraints."""
    # Read current constraints from pyproject.toml
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    try:
        with open(pyproject_path, 'r') as f:
            content = f.read()
    except Exception:
        return "unknown", "Could not read pyproject.toml"
    
    # Define version constraints from our pyproject.toml
    constraints = {
        'numpy': '<2.0.0',
        'black': '<25.0.0',
        'isort': '<6.0.0',
        'pytest-cov': '<6.0.0',
        'pre-commit': '<4.0.0',
        'biopython': '<2.0.0',
        'matplotlib': '<4.0.0',
        'pytest': '<9.0.0',
        'flake8': '<8.0.0',
        'mypy': '<2.0.0',
        'bandit': '<2.0.0',
        'jupyter': '<2.0.0',
        'toml': '<1.0.0',
    }
    
    if package in constraints:
        constraint = constraints[package]
        
        # Simple version comparison (works for most cases)
        if '<' in constraint:
            max_version = constraint.replace('<', '').strip()
            
            # Compare major versions
            try:
                new_major = int(new_version.split('.')[0])
                max_major = int(max_version.split('.')[0])
                
                if new_major >= max_major:
                    return "incompatible", f"Exceeds constraint {constraint}"
                else:
                    return "compatible", "Within version constraints"
            except ValueError:
                return "unknown", "Could not parse version numbers"
    
    # GitHub Actions don't have explicit constraints, generally safe to update
    if dep_type == "github_actions":
        return "safe", "GitHub Actions update"
    
    return "unknown", "No explicit constraint found"


def categorize_prs(prs):
    """Categorize PRs by safety and type."""
    categories = {
        'safe_to_merge': [],
        'needs_constraint_update': [],
        'needs_testing': [],
        'unknown': []
    }
    
    for pr in prs:
        update_info = parse_dependency_update(pr['title'])
        if not update_info:
            categories['unknown'].append(pr)
            continue
        
        compatibility, reason = check_version_compatibility(
            update_info['package'], 
            update_info['new_version'], 
            update_info['type']
        )
        
        pr['update_info'] = update_info
        pr['compatibility'] = compatibility
        pr['reason'] = reason
        
        if compatibility == "safe" or compatibility == "compatible":
            categories['safe_to_merge'].append(pr)
        elif compatibility == "incompatible":
            categories['needs_constraint_update'].append(pr)
        else:
            categories['needs_testing'].append(pr)
    
    return categories


def print_pr_summary(categories):
    """Print a summary of PRs by category."""
    print("🔍 Dependabot PR Analysis")
    print("=" * 50)
    
    total_prs = sum(len(prs) for prs in categories.values())
    print(f"Total PRs: {total_prs}")
    print()
    
    for category, prs in categories.items():
        if not prs:
            continue
            
        category_name = category.replace('_', ' ').title()
        print(f"📋 {category_name} ({len(prs)} PRs):")
        print("-" * 30)
        
        for pr in prs:
            print(f"  #{pr['number']}: {pr['title']}")
            if 'update_info' in pr:
                info = pr['update_info']
                print(f"    Package: {info['package']}")
                print(f"    Version: {info['old_version']} → {info['new_version']}")
                print(f"    Type: {info['type']}")
                print(f"    Status: {pr['compatibility']} - {pr['reason']}")
            print(f"    URL: {pr['url']}")
            print()


def generate_action_plan(categories):
    """Generate an action plan for handling the PRs."""
    print("🎯 Recommended Action Plan")
    print("=" * 50)
    
    # Safe to merge
    safe_prs = categories['safe_to_merge']
    if safe_prs:
        print(f"✅ STEP 1: Merge Safe PRs ({len(safe_prs)} PRs)")
        print("These can be merged immediately:")
        for pr in safe_prs:
            print(f"  - #{pr['number']}: {pr['update_info']['package']}")
        print()
        print("Commands:")
        for pr in safe_prs:
            print(f"  gh pr merge {pr['number']} --squash --delete-branch")
        print()
    
    # Need constraint updates
    constraint_prs = categories['needs_constraint_update']
    if constraint_prs:
        print(f"🔧 STEP 2: Update Constraints ({len(constraint_prs)} PRs)")
        print("These need pyproject.toml constraint updates:")
        for pr in constraint_prs:
            info = pr['update_info']
            print(f"  - #{pr['number']}: {info['package']} {info['old_version']} → {info['new_version']}")
        print()
        print("Required pyproject.toml updates:")
        for pr in constraint_prs:
            info = pr['update_info']
            package = info['package']
            new_version = info['new_version']
            new_major = new_version.split('.')[0]
            next_major = str(int(new_major) + 1)
            print(f"  - {package}: \">={info['old_version']},<{next_major}.0.0\"")
        print()
    
    # Need testing
    testing_prs = categories['needs_testing']
    if testing_prs:
        print(f"🧪 STEP 3: Test Carefully ({len(testing_prs)} PRs)")
        print("These need manual testing:")
        for pr in testing_prs:
            print(f"  - #{pr['number']}: {pr['title']}")
        print()
    
    # Unknown
    unknown_prs = categories['unknown']
    if unknown_prs:
        print(f"❓ STEP 4: Manual Review ({len(unknown_prs)} PRs)")
        print("These need manual review:")
        for pr in unknown_prs:
            print(f"  - #{pr['number']}: {pr['title']}")
        print()


def main():
    """Main function."""
    print("🤖 Dependabot PR Handler")
    print("=" * 50)
    
    # Get all Dependabot PRs
    prs = get_dependabot_prs()
    if not prs:
        print("✅ No open Dependabot PRs found!")
        return
    
    print(f"Found {len(prs)} open Dependabot PRs")
    print()
    
    # Categorize PRs
    categories = categorize_prs(prs)
    
    # Print summary
    print_pr_summary(categories)
    
    # Generate action plan
    generate_action_plan(categories)
    
    print("💡 Tips:")
    print("- Always run tests after merging dependency updates")
    print("- Consider updating constraints to allow patch/minor updates")
    print("- GitHub Actions updates are generally safe")
    print("- Major version bumps may have breaking changes")


if __name__ == "__main__":
    main()
