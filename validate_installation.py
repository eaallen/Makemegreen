#!/usr/bin/env python3
"""
Validation script for GitHub Contributions CLI
This script validates that all components are working correctly
"""

import sys
import os
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - PASSED")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def validate_imports():
    """Validate that all required modules can be imported"""
    print("\n📦 Validating imports...")
    
    try:
        from github_contributions_cli.main import main
        from github_contributions_cli.contributor import GitHubContributor
        from github_contributions_cli.utils import (
            validate_github_token, 
            generate_random_content, 
            get_random_commit_message
        )
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def validate_utilities():
    """Validate utility functions work correctly"""
    print("\n🛠️  Validating utility functions...")
    
    try:
        from github_contributions_cli.utils import generate_random_content, get_random_commit_message
        
        # Test content generation
        content = generate_random_content()
        assert isinstance(content, str)
        assert len(content) > 0
        assert '[' in content and ']' in content  # Should have timestamp
        
        # Test commit message generation
        message = get_random_commit_message()
        assert isinstance(message, str)
        assert len(message) > 0
        assert any(ord(char) > 127 for char in message)  # Should have emoji
        
        print("✅ Utility functions working correctly")
        return True
    except Exception as e:
        print(f"❌ Utility function error: {e}")
        return False

def validate_cli_help():
    """Validate CLI help command works"""
    return run_command(
        "python3 -m github_contributions_cli.main --help",
        "CLI help command"
    )

def validate_tests():
    """Validate all tests pass"""
    return run_command(
        "python3 -m pytest tests/ -v --tb=short",
        "Running test suite"
    )

def validate_package_structure():
    """Validate package structure is correct"""
    print("\n📁 Validating package structure...")
    
    required_files = [
        "setup.py",
        "requirements.txt",
        "README.md",
        "github_contributions_cli/__init__.py",
        "github_contributions_cli/main.py",
        "github_contributions_cli/contributor.py",
        "github_contributions_cli/utils.py",
        "tests/__init__.py",
        "tests/test_contributor.py",
        "tests/test_utils.py",
        "tests/test_integration.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Main validation function"""
    print("🎄 GitHub Contributions CLI - Installation Validation")
    print("=" * 60)
    
    validations = [
        ("Package Structure", validate_package_structure),
        ("Imports", validate_imports),
        ("Utility Functions", validate_utilities),
        ("CLI Help", validate_cli_help),
        ("Test Suite", validate_tests)
    ]
    
    results = []
    for name, validation_func in validations:
        result = validation_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} validations passed")
    
    if passed == total:
        print("\n🎉 All validations passed! The CLI is ready to use.")
        print("\nTo get started:")
        print("1. Set your GitHub token: export GITHUB_TOKEN=your_token_here")
        print("2. Run the CLI: python3 -m github_contributions_cli.main --dry-run")
        return True
    else:
        print(f"\n⚠️  {total - passed} validation(s) failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)