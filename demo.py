#!/usr/bin/env python3
"""
Demo script showing the GitHub Contributions CLI in action
"""

import os
import sys
from github_contributions_cli.utils import generate_random_content, get_random_commit_message

def demo_utilities():
    """Demonstrate the utility functions"""
    print("🎄 GitHub Contributions CLI - Demo")
    print("=" * 50)
    
    print("\n📝 Random Content Generation:")
    print("-" * 30)
    for i in range(5):
        content = generate_random_content()
        print(f"{i+1:2d}. {content}")
    
    print("\n💬 Random Commit Messages:")
    print("-" * 30)
    for i in range(5):
        message = get_random_commit_message()
        print(f"{i+1:2d}. {message}")
    
    print("\n🔧 CLI Usage Examples:")
    print("-" * 30)
    print("1. Basic usage (random 1-15 commits):")
    print("   python3 -m github_contributions_cli.main")
    print()
    print("2. Specify repository and commits:")
    print("   python3 -m github_contributions_cli.main --repo myrepo --commits 5")
    print()
    print("3. Dry run (see what would happen):")
    print("   python3 -m github_contributions_cli.main --dry-run")
    print()
    print("4. Verbose output:")
    print("   python3 -m github_contributions_cli.main --verbose")
    print()
    print("5. Help:")
    print("   python3 -m github_contributions_cli.main --help")
    
    print("\n📋 Setup Instructions:")
    print("-" * 30)
    print("1. Get a GitHub Personal Access Token:")
    print("   - Go to GitHub Settings > Developer settings > Personal access tokens")
    print("   - Generate a new token with 'repo' permissions")
    print()
    print("2. Set the environment variable:")
    print("   export GITHUB_TOKEN=your_token_here")
    print()
    print("3. Run the CLI:")
    print("   python3 -m github_contributions_cli.main --dry-run")
    
    print("\n🎯 What the CLI does:")
    print("-" * 30)
    print("• Creates or uses the specified GitHub repository")
    print("• Generates 1-15 random commits per day")
    print("• Adds Christmas-themed content to 'mytree.txt'")
    print("• Uses festive commit messages with emojis")
    print("• Spreads commits across different days")
    print("• Pushes everything to the main branch")
    
    print("\n✨ Features:")
    print("-" * 30)
    print("• 🎄 Christmas-themed content and messages")
    print("• 🔧 Simple CLI interface with sensible defaults")
    print("• 🛡️  Dry-run mode for safe testing")
    print("• 🧪 Comprehensive test suite")
    print("• 📊 GitHub API integration")
    print("• 🎯 Random commit timing and content")
    
    print("\n🎉 Ready to make your GitHub chart green like a Christmas tree!")

if __name__ == "__main__":
    demo_utilities()