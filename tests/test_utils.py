"""
Tests for utility functions
"""

import unittest
from unittest.mock import patch, Mock
from github_contributions_cli.utils import (
    validate_github_token, 
    generate_random_content, 
    get_random_commit_message,
    get_random_commit_times
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""
    
    @patch('github_contributions_cli.utils.Github')
    def test_validate_github_token_valid(self, mock_github_class):
        """Test token validation with valid token"""
        mock_github = Mock()
        mock_user = Mock()
        mock_github.get_user.return_value = mock_user
        mock_github_class.return_value = mock_github
        
        result = validate_github_token("valid_token")
        
        self.assertTrue(result)
        # Check that Github was called with auth parameter
        mock_github_class.assert_called_once()
        call_args = mock_github_class.call_args
        self.assertIn('auth', call_args.kwargs)
        from github import Auth
        self.assertIsInstance(call_args.kwargs['auth'], Auth.Token)
        mock_github.get_user.assert_called_once()
    
    @patch('github_contributions_cli.utils.Github')
    def test_validate_github_token_invalid(self, mock_github_class):
        """Test token validation with invalid token"""
        from github import GithubException
        
        mock_github = Mock()
        mock_github.get_user.side_effect = GithubException(401, "Bad credentials")
        mock_github_class.return_value = mock_github
        
        result = validate_github_token("invalid_token")
        
        self.assertFalse(result)
    
    def test_generate_random_content_structure(self):
        """Test that generated content has expected structure"""
        content = generate_random_content()
        
        # Should contain timestamp in brackets
        self.assertIn('[', content)
        self.assertIn(']', content)
        
        # Should contain some non-ASCII characters (emojis)
        self.assertTrue(any(ord(char) > 127 for char in content))
        
        # Should be a reasonable length
        self.assertGreater(len(content), 10)
        self.assertLess(len(content), 200)
    
    def test_generate_random_content_uniqueness(self):
        """Test that multiple generations produce different content"""
        contents = [generate_random_content() for _ in range(5)]
        
        # All should be different
        self.assertEqual(len(contents), len(set(contents)))
    
    def test_get_random_commit_message_structure(self):
        """Test that commit messages have expected structure"""
        message = get_random_commit_message()
        
        # Should contain emoji
        self.assertTrue(any(ord(char) > 127 for char in message))
        
        # Should be reasonable length
        self.assertGreater(len(message), 5)
        self.assertLess(len(message), 100)
    
    def test_get_random_commit_message_variety(self):
        """Test that multiple message generations produce variety"""
        messages = [get_random_commit_message() for _ in range(20)]
        
        # Should have some variety
        unique_messages = set(messages)
        self.assertGreater(len(unique_messages), 1)
    
    def test_get_random_commit_times(self):
        """Test commit time generation"""
        times = get_random_commit_times(5)
        
        # Should return correct number of times
        self.assertEqual(len(times), 5)
        
        # All should be valid datetime strings
        from datetime import datetime
        for time_str in times:
            try:
                datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                self.fail(f"Invalid datetime string: {time_str}")
    
    def test_get_random_commit_times_variety(self):
        """Test that commit times have variety"""
        times = get_random_commit_times(10)
        
        # Should have some variety (not all the same)
        unique_times = set(times)
        self.assertGreater(len(unique_times), 1)


if __name__ == '__main__':
    unittest.main()