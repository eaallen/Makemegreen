"""
Integration tests for GitHub Contributions CLI
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
import tempfile
import os
import sys
from io import StringIO

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from github_contributions_cli.main import main
from github_contributions_cli.contributor import GitHubContributor


class TestIntegration(unittest.TestCase):
    """Integration tests for the CLI"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
    
    def tearDown(self):
        """Clean up after tests"""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
    
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'fake_token'})
    @patch('github_contributions_cli.main.GitHubContributor')
    @patch('github_contributions_cli.main.validate_github_token')
    def test_main_dry_run(self, mock_validate, mock_contributor_class):
        """Test main function in dry run mode"""
        mock_validate.return_value = True
        mock_contributor = Mock()
        mock_contributor_class.return_value = mock_contributor
        mock_contributor.make_contributions.return_value = {
            'success': True,
            'commits_made': 3,
            'repo_url': 'https://github.com/test/repo'
        }
        
        # Test with dry run
        with patch('sys.argv', ['main.py', '--dry-run', '--repo', 'testrepo']):
            try:
                main()
            except SystemExit:
                pass
        
        # Check that contributor was called with dry_run=True
        mock_contributor.make_contributions.assert_called_once()
        call_args = mock_contributor.make_contributions.call_args
        self.assertTrue(call_args[1]['dry_run'])
    
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'fake_token'})
    @patch('github_contributions_cli.main.validate_github_token')
    def test_main_no_token(self, mock_validate):
        """Test main function without GitHub token"""
        # Remove token from environment
        if 'GITHUB_TOKEN' in os.environ:
            del os.environ['GITHUB_TOKEN']
        
        with patch('sys.argv', ['main.py', '--dry-run']):
            with self.assertRaises(SystemExit) as cm:
                main()
            
            self.assertEqual(cm.exception.code, 1)
    
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'fake_token'})
    @patch('github_contributions_cli.main.validate_github_token')
    def test_main_invalid_token(self, mock_validate):
        """Test main function with invalid token"""
        mock_validate.return_value = False
        
        with patch('sys.argv', ['main.py', '--dry-run']):
            with self.assertRaises(SystemExit) as cm:
                main()
            
            self.assertEqual(cm.exception.code, 1)
    
    @patch.dict(os.environ, {'GITHUB_TOKEN': 'fake_token'})
    @patch('github_contributions_cli.main.GitHubContributor')
    @patch('github_contributions_cli.main.validate_github_token')
    def test_main_with_commits_option(self, mock_validate, mock_contributor_class):
        """Test main function with specific number of commits"""
        mock_validate.return_value = True
        mock_contributor = Mock()
        mock_contributor_class.return_value = mock_contributor
        mock_contributor.make_contributions.return_value = {
            'success': True,
            'commits_made': 5,
            'repo_url': 'https://github.com/test/repo'
        }
        
        with patch('sys.argv', ['main.py', '--dry-run', '--commits', '5']):
            try:
                main()
            except SystemExit:
                pass
        
        # Check that contributor was called with 5 commits
        call_args = mock_contributor.make_contributions.call_args
        self.assertEqual(call_args[1]['num_commits'], 5)


class TestContributorIntegration(unittest.TestCase):
    """Integration tests for GitHubContributor"""
    
    @patch('github_contributions_cli.contributor.Github')
    def test_contributor_initialization(self, mock_github_class):
        """Test contributor initialization with mocked GitHub"""
        mock_github = Mock()
        mock_user = Mock()
        mock_user.login = "testuser"
        mock_github.get_user.return_value = mock_user
        mock_github_class.return_value = mock_github
        
        contributor = GitHubContributor("fake_token", "testuser")
        
        self.assertEqual(contributor.owner, "testuser")
        # Check that Github was called with auth parameter
        mock_github_class.assert_called_once()
        call_args = mock_github_class.call_args
        self.assertIn('auth', call_args.kwargs)
        from github import Auth
        self.assertIsInstance(call_args.kwargs['auth'], Auth.Token)
    
    @patch('github_contributions_cli.contributor.Github')
    def test_contributor_auto_owner(self, mock_github_class):
        """Test contributor initialization with auto-detected owner"""
        mock_github = Mock()
        mock_user = Mock()
        mock_user.login = "authenticated_user"
        mock_github.get_user.return_value = mock_user
        mock_github_class.return_value = mock_github
        
        contributor = GitHubContributor("fake_token")
        
        self.assertEqual(contributor.owner, "authenticated_user")


if __name__ == '__main__':
    unittest.main()