"""
Tests for GitHub Contributor module
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
from github_contributions_cli.contributor import GitHubContributor
from github_contributions_cli.utils import generate_random_content, get_random_commit_message


class TestGitHubContributor(unittest.TestCase):
    """Test cases for GitHubContributor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_token = "fake_token_123"
        self.mock_owner = "testuser"
        self.contributor = GitHubContributor(self.mock_token, self.mock_owner)
    
    @patch('github_contributions_cli.contributor.Github')
    def test_init(self, mock_github_class):
        """Test GitHubContributor initialization"""
        mock_github = Mock()
        mock_github_class.return_value = mock_github
        mock_github.get_user.return_value.login = "testuser"
        
        contributor = GitHubContributor("fake_token", "testuser")
        
        self.assertEqual(contributor.owner, "testuser")
        # Check that Github was called with auth parameter
        mock_github_class.assert_called_once()
        call_args = mock_github_class.call_args
        self.assertIn('auth', call_args.kwargs)
        from github import Auth
        self.assertIsInstance(call_args.kwargs['auth'], Auth.Token)
    
    @patch('github_contributions_cli.contributor.Github')
    def test_init_without_owner(self, mock_github_class):
        """Test GitHubContributor initialization without owner"""
        mock_github = Mock()
        mock_user = Mock()
        mock_user.login = "authenticated_user"
        mock_github.get_user.return_value = mock_user
        mock_github_class.return_value = mock_github
        
        contributor = GitHubContributor("fake_token")
        
        self.assertEqual(contributor.owner, "authenticated_user")
    
    @patch('github_contributions_cli.contributor.Github')
    @patch('tempfile.mkdtemp')
    @patch('os.system')
    @patch('os.chdir')
    @patch('builtins.open', create=True)
    def test_make_contributions_dry_run(self, mock_open, mock_chdir, mock_system, mock_mkdtemp, mock_github_class):
        """Test make_contributions in dry run mode"""
        mock_github = Mock()
        mock_repo = Mock()
        mock_repo.html_url = "https://github.com/testuser/testrepo"
        mock_github.get_repo.return_value = mock_repo
        mock_github_class.return_value = mock_github
        
        contributor = GitHubContributor("fake_token", "testuser")
        result = contributor.make_contributions("testrepo", 3, dry_run=True)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['commits_made'], 3)
        self.assertEqual(result['repo_url'], "https://github.com/testuser/testrepo")
        self.assertIn('Would make', result['message'])
    
    @patch('github_contributions_cli.contributor.Github')
    def test_make_contributions_repo_not_found(self, mock_github_class):
        """Test make_contributions when repository doesn't exist"""
        from github import GithubException
        
        mock_github = Mock()
        mock_github.get_repo.side_effect = GithubException(404, "Not Found")
        mock_github_class.return_value = mock_github
        
        contributor = GitHubContributor("fake_token", "testuser")
        result = contributor.make_contributions("nonexistent", 1, dry_run=True)
        
        self.assertFalse(result['success'])
        self.assertIn('Could not access repository', result['error'])


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_generate_random_content(self):
        """Test random content generation"""
        content = generate_random_content()
        
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)
        # Should contain timestamp
        self.assertIn('[', content)
        self.assertIn(']', content)
    
    def test_get_random_commit_message(self):
        """Test random commit message generation"""
        message = get_random_commit_message()
        
        self.assertIsInstance(message, str)
        self.assertGreater(len(message), 0)
        # Should contain emoji
        self.assertTrue(any(ord(char) > 127 for char in message))
    
    def test_generate_multiple_contents(self):
        """Test that multiple content generations are different"""
        content1 = generate_random_content()
        content2 = generate_random_content()
        
        # They should be different (very high probability)
        self.assertNotEqual(content1, content2)
    
    def test_generate_multiple_messages(self):
        """Test that multiple message generations are different"""
        messages = [get_random_commit_message() for _ in range(10)]
        
        # Should have some variety (not all the same)
        unique_messages = set(messages)
        self.assertGreater(len(unique_messages), 1)


if __name__ == '__main__':
    unittest.main()