# GitHub Contributions CLI 🎄

A Python CLI tool to automate GitHub contributions and make your chart green like a Christmas tree! This tool helps you maintain a consistent contribution streak by automatically creating commits to a specified repository.

## Features

- 🎯 **Automated Commits**: Creates 1-15 random commits per day
- 🌲 **Christmas Theme**: Adds festive content to `mytree.txt` file
- 🔧 **Easy Setup**: Simple CLI interface with sensible defaults
- 🛡️ **Safe Operation**: Dry-run mode to preview changes
- 🧪 **Well Tested**: Comprehensive test suite included
- 📊 **GitHub Integration**: Direct integration with GitHub API

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd github-contributions-cli
```

2. Install the package:
```bash
pip install -e .
```

3. Set up your GitHub token:
```bash
export GITHUB_TOKEN=your_github_personal_access_token
```

## Usage

### Basic Usage

Make contributions to the default repository:
```bash
github-contributions
```

### Advanced Usage

```bash
# Specify repository name
github-contributions --repo my-awesome-repo

# Specify number of commits (instead of random 1-15)
github-contributions --commits 10

# Specify repository owner
github-contributions --owner myusername --repo myrepo

# Dry run (see what would happen without making changes)
github-contributions --dry-run

# Verbose output
github-contributions --verbose
```

### Command Line Options

- `--repo, -r`: GitHub repository name (default: "makemegreenlikeChristmas")
- `--owner, -o`: GitHub repository owner (defaults to authenticated user)
- `--commits, -c`: Number of commits to make (random 1-15 if not specified)
- `--dry-run`: Show what would be done without making actual changes
- `--verbose, -v`: Enable verbose output

## How It Works

1. **Repository Setup**: The tool will create the specified repository if it doesn't exist
2. **Content Generation**: For each commit, it adds random Christmas-themed content to `mytree.txt`
3. **Commit Creation**: Creates commits with festive messages and timestamps
4. **GitHub Push**: Pushes all commits to the main branch

## Example Output

```
🎄 Making 8 commits to repository: makemegreenlikeChristmas
✅ Commit 1/8: 🎄 Add festive content to mytree.txt
✅ Commit 2/8: ✨ Update Christmas tree with new decorations
✅ Commit 3/8: 🎁 Add holiday cheer to the repository
✅ Commit 4/8: 🌟 Spread some Christmas magic
✅ Commit 5/8: ❄️ Add winter wonderland content
✅ Commit 6/8: 🎅 Santa's workshop update
✅ Commit 7/8: 🔔 Ring in the holiday spirit
✅ Commit 8/8: 🎊 Celebrate the season
✅ Successfully made 8 commits!
📁 Repository: https://github.com/yourusername/makemegreenlikeChristmas
🎉 Your GitHub chart should be looking greener now!
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=github_contributions_cli

# Run specific test file
python -m pytest tests/test_contributor.py
```

### Project Structure

```
github-contributions-cli/
├── github_contributions_cli/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── contributor.py       # Core GitHub operations
│   └── utils.py             # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_contributor.py  # Unit tests for contributor
│   ├── test_utils.py        # Unit tests for utilities
│   └── test_integration.py  # Integration tests
├── setup.py                 # Package setup
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Requirements

- Python 3.8+
- GitHub Personal Access Token
- Git (for repository operations)

## Dependencies

- `requests`: HTTP library for API calls
- `PyGithub`: Python wrapper for GitHub API
- `click`: Command-line interface framework
- `python-dotenv`: Environment variable management

## Security Notes

- Your GitHub token is only used for repository operations
- The tool only creates/modifies the `mytree.txt` file
- All operations are logged for transparency
- Use dry-run mode to preview changes before applying

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational and personal use. Please use responsibly and in accordance with GitHub's Terms of Service. The goal is to help maintain consistent coding habits, not to artificially inflate contribution statistics.

---

Made with ❤️ and 🎄 for the GitHub community!