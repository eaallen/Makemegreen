#!/usr/bin/env python3
"""
Main CLI module for GitHub Contributions tool
"""

import click
import os
import sys
from datetime import datetime, timedelta
from .contributor import GitHubContributor
from .utils import validate_github_token, setup_logging


@click.command()
@click.option(
    '--repo', 
    '-r', 
    default='makemegreenlikeChristmas',
    help='GitHub repository name (default: makemegreenlikeChristmas)'
)
@click.option(
    '--owner',
    '-o',
    help='GitHub repository owner (defaults to authenticated user)'
)
@click.option(
    '--commits',
    '-c',
    type=int,
    help='Number of commits to make (random 1-15 if not specified)'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Show what would be done without making actual changes'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Enable verbose output'
)
def main(repo, owner, commits, dry_run, verbose):
    """
    Make your GitHub contributions chart green like a Christmas tree! 🌲
    
    This tool will create commits to your specified repository to boost your
    GitHub contributions chart.
    """
    setup_logging(verbose)
    
    # Validate GitHub token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        click.echo("❌ Error: GITHUB_TOKEN environment variable is required", err=True)
        click.echo("Please set your GitHub personal access token:", err=True)
        click.echo("export GITHUB_TOKEN=your_token_here", err=True)
        sys.exit(1)
    
    if not validate_github_token(token):
        click.echo("❌ Error: Invalid GitHub token", err=True)
        sys.exit(1)
    
    # Initialize contributor
    try:
        contributor = GitHubContributor(token, owner)
    except Exception as e:
        click.echo(f"❌ Error initializing GitHub contributor: {e}", err=True)
        sys.exit(1)
    
    # Determine number of commits
    if commits is None:
        import random
        commits = random.randint(1, 15)
    
    click.echo(f"🎄 Making {commits} commits to repository: {repo}")
    
    if dry_run:
        click.echo("🔍 DRY RUN MODE - No actual changes will be made")
    
    try:
        # Make contributions
        result = contributor.make_contributions(
            repo_name=repo,
            num_commits=commits,
            dry_run=dry_run
        )
        
        if result['success']:
            click.echo(f"✅ Successfully made {result['commits_made']} commits!")
            click.echo(f"📁 Repository: {result['repo_url']}")
            click.echo("🎉 Your GitHub chart should be looking greener now!")
        else:
            click.echo(f"❌ Error: {result['error']}", err=True)
            sys.exit(1)
            
    except KeyboardInterrupt:
        click.echo("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()