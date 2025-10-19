"""
Utility functions for GitHub Contributions CLI
"""

import os
import random
import string
import logging
from typing import List
from github import Github, GithubException, Auth


def validate_github_token(token: str) -> bool:
    """
    Validate if the GitHub token is valid
    
    Args:
        token: GitHub personal access token
        
    Returns:
        True if token is valid, False otherwise
    """
    try:
        github = Github(auth=Auth.Token(token))
        # Try to get authenticated user
        user = github.get_user()
        return user is not None
    except GithubException:
        return False


def generate_random_content() -> str:
    """
    Generate random content for the mytree.txt file
    
    Returns:
        Random string content
    """
    # Christmas-themed content options
    christmas_emojis = ['🎄', '🎅', '❄️', '⛄', '🎁', '🌟', '✨', '🔔', '🎊', '🎉']
    christmas_words = [
        'Christmas', 'holiday', 'festive', 'jolly', 'merry', 'cheerful',
        'winter', 'snow', 'gift', 'present', 'decorations', 'ornaments',
        'carol', 'song', 'celebration', 'family', 'joy', 'peace'
    ]
    
    # Generate random content
    content_parts = []
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    content_parts.append(f"[{timestamp}]")
    
    # Add random emoji
    content_parts.append(random.choice(christmas_emojis))
    
    # Add random Christmas word
    content_parts.append(random.choice(christmas_words))
    
    # Add random characters
    random_chars = ''.join(random.choices(
        string.ascii_letters + string.digits + ' ', 
        k=random.randint(10, 50)
    ))
    content_parts.append(random_chars)
    
    return ' '.join(content_parts)


def get_random_commit_message() -> str:
    """
    Generate a random commit message
    
    Returns:
        Random commit message
    """
    commit_messages = [
        "🎄 Add festive content to mytree.txt",
        "✨ Update Christmas tree with new decorations",
        "🎁 Add holiday cheer to the repository",
        "🌟 Spread some Christmas magic",
        "❄️ Add winter wonderland content",
        "🎅 Santa's workshop update",
        "🔔 Ring in the holiday spirit",
        "🎊 Celebrate the season",
        "✨ Add sparkle to the codebase",
        "🎉 Holiday happiness update",
        "🌲 Make the tree greener",
        "🎄 Christmas contribution",
        "🌟 Starry night update",
        "❄️ Snowy day commit",
        "🎁 Gift of code",
        "🔔 Jingle bells update",
        "🎊 Party time commit",
        "✨ Magical moment",
        "🎉 Celebration time",
        "🌲 Forest of commits"
    ]
    
    return random.choice(commit_messages)


def setup_logging(verbose: bool = False) -> None:
    """
    Setup logging configuration
    
    Args:
        verbose: Enable verbose logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_random_commit_times(num_commits: int) -> List[str]:
    """
    Generate random commit times spread across different days
    
    Args:
        num_commits: Number of commits to generate times for
        
    Returns:
        List of datetime strings for commits
    """
    from datetime import datetime, timedelta
    
    times = []
    base_date = datetime.now()
    
    for i in range(num_commits):
        # Spread commits across the last 7 days
        days_ago = random.randint(0, 6)
        hours = random.randint(9, 23)  # Business hours
        minutes = random.randint(0, 59)
        seconds = random.randint(0, 59)
        
        commit_time = base_date - timedelta(
            days=days_ago,
            hours=base_date.hour - hours,
            minutes=base_date.minute - minutes,
            seconds=base_date.second - seconds
        )
        
        times.append(commit_time.strftime('%Y-%m-%d %H:%M:%S'))
    
    return times