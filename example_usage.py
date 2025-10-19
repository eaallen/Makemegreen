#!/usr/bin/env python3
"""
Example usage of GitHub Contributions CLI
"""

import os
import sys
from github_contributions_cli.contributor import GitHubContributor
from github_contributions_cli.utils import validate_github_token, generate_random_content, get_random_commit_message

def example_usage():
    """Demonstrate the CLI functionality"""
    print("🎄 GitHub Contributions CLI Example")
    print("=" * 40)
    
    # Check for GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ Please set GITHUB_TOKEN environment variable")
        print("export GITHUB_TOKEN=your_token_here")
        return
    
    # Validate token
    if not validate_github_token(token):
        print("❌ Invalid GitHub token")
        return
    
    print("✅ GitHub token is valid")
    
    # Show utility functions
    print("\n📝 Generated random content:")
    for i in range(3):
        content = generate_random_content()
        print(f"  {i+1}. {content}")
    
    print("\n💬 Generated commit messages:")
    for i in range(3):
        message = get_random_commit_message()
        print(f"  {i+1}. {message}")
    
    # Show what would happen in dry run
    print("\n🔍 Dry run example:")
    try:
        contributor = GitHubContributor(token)
        result = contributor.make_contributions(
            repo_name="example-repo",
            num_commits=3,
            dry_run=True
        )
        
        if result['success']:
            print(f"✅ Would make {result['commits_made']} commits")
            print(f"📁 Repository: {result['repo_url']}")
        else:
            print(f"❌ Error: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    example_usage()