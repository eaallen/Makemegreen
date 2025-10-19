"""
GitHub Contributor module for automating contributions
"""

import os
import random
import string
import tempfile
import shutil
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from github import Github, GithubException, Auth
from github.Repository import Repository
from .utils import generate_random_content, get_random_commit_message


class GitHubContributor:
    """Handles GitHub repository operations for contribution automation"""
    
    def __init__(self, token: str, owner: Optional[str] = None):
        """
        Initialize the GitHub contributor
        
        Args:
            token: GitHub personal access token
            owner: Repository owner (defaults to authenticated user)
        """
        self.github = Github(auth=Auth.Token(token))
        self.owner = owner or self.github.get_user().login
        self.temp_dir = None
        
    def make_contributions(
        self, 
        repo_name: str, 
        num_commits: int, 
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Make contributions to the specified repository
        
        Args:
            repo_name: Name of the repository
            num_commits: Number of commits to make
            dry_run: If True, don't make actual changes
            
        Returns:
            Dictionary with operation results
        """
        try:
            # Get or create repository
            repo = self._get_or_create_repo(repo_name, dry_run)
            if not repo:
                return {
                    'success': False,
                    'error': f'Could not access repository {self.owner}/{repo_name}'
                }
            
            if dry_run:
                return {
                    'success': True,
                    'commits_made': num_commits,
                    'repo_url': repo.html_url,
                    'message': f'Would make {num_commits} commits to {repo.html_url}'
                }
            
            # Clone repository to temporary directory
            self.temp_dir = tempfile.mkdtemp(prefix=f'github_contrib_{repo_name}_')
            
            # Clone the repository
            clone_url = repo.clone_url.replace('https://', f'https://{self.github._Github__requester._Requester__authorizationHeader.split()[1]}@')
            os.system(f'git clone {clone_url} {self.temp_dir}')
            
            # Make commits
            commits_made = self._make_commits(repo, num_commits)
            
            # Cleanup
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            
            return {
                'success': True,
                'commits_made': commits_made,
                'repo_url': repo.html_url
            }
            
        except Exception as e:
            # Cleanup on error
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_or_create_repo(self, repo_name: str, dry_run: bool = False) -> Optional[Repository]:
        """Get existing repository or create a new one"""
        try:
            # Try to get existing repository
            repo = self.github.get_repo(f"{self.owner}/{repo_name}")
            return repo
        except GithubException as e:
            if e.status == 404:
                # Repository doesn't exist, create it
                if dry_run:
                    print(f"Would create repository: {self.owner}/{repo_name}")
                    return None
                
                try:
                    repo = self.github.get_user().create_repo(
                        repo_name,
                        description="A repository to make my GitHub chart green like a Christmas tree! 🎄",
                        private=False,
                        auto_init=True
                    )
                    print(f"✅ Created repository: {repo.html_url}")
                    return repo
                except GithubException as create_error:
                    print(f"❌ Error creating repository: {create_error}")
                    return None
            else:
                print(f"❌ Error accessing repository: {e}")
                return None
    
    def _make_commits(self, repo: Repository, num_commits: int) -> int:
        """Make the actual commits to the repository"""
        commits_made = 0
        
        for i in range(num_commits):
            try:
                # Generate random content for mytree.txt
                content = generate_random_content()
                
                # Write to mytree.txt
                tree_file_path = os.path.join(self.temp_dir, 'mytree.txt')
                with open(tree_file_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n{content}")
                
                # Add and commit
                os.chdir(self.temp_dir)
                os.system('git add mytree.txt')
                
                # Generate commit message
                commit_message = get_random_commit_message()
                
                # Make commit with specific date to spread across different days
                commit_date = datetime.now() - timedelta(days=random.randint(0, 7))
                date_str = commit_date.strftime('%Y-%m-%d %H:%M:%S')
                
                os.system(f'git commit -m "{commit_message}" --date="{date_str}"')
                
                # Push to main branch
                os.system('git push origin main')
                
                commits_made += 1
                print(f"✅ Commit {i+1}/{num_commits}: {commit_message}")
                
                # Small delay to avoid rate limiting
                import time
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error making commit {i+1}: {e}")
                continue
        
        return commits_made