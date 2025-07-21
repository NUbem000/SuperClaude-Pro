# Contributing to SuperClaude Pro

## 🌟 Welcome Contributors!

We're excited that you're interested in contributing to SuperClaude Pro! This document provides guidelines and instructions for contributing to the project.

## 📝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- GitHub account
- Basic knowledge of Python and Git

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the 'Fork' button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/SuperClaude-Pro.git
   cd SuperClaude-Pro
   ```

3. **Set up development environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install in development mode
   pip install -e ".[dev,docs,telemetry]"
   
   # Install pre-commit hooks
   pre-commit install
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🎯 Contribution Guidelines

### Types of Contributions

#### 🐛 Bug Reports
- Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml)
- Include detailed steps to reproduce
- Provide system information
- Add relevant logs or screenshots

#### ✨ Feature Requests
- Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml)
- Explain the problem your feature solves
- Provide use cases
- Consider implementation details

#### 📝 Documentation
- Fix typos or clarify existing docs
- Add examples
- Improve API documentation
- Translate documentation

#### 💻 Code Contributions
- Fix bugs
- Implement new features
- Improve performance
- Add tests

### Pull Request Process

1. **Before starting work**
   - Check existing issues and PRs
   - Create an issue if none exists
   - Get feedback on your approach

2. **While developing**
   - Follow our coding standards
   - Write tests for new functionality
   - Update documentation
   - Keep commits focused and atomic

3. **Before submitting**
   ```bash
   # Run all checks
   make check
   
   # Format code
   make format
   
   # Run tests
   make test-cov
   ```

4. **Submitting PR**
   - Use a descriptive title
   - Reference related issues
   - Complete the PR template
   - Ensure CI passes

### Coding Standards

#### Python Style
- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use meaningful variable names

#### Example:
```python
def calculate_score(items: List[Item], multiplier: float = 1.0) -> float:
    """Calculate the total score for items.
    
    Args:
        items: List of items to score
        multiplier: Score multiplier (default: 1.0)
        
    Returns:
        Total calculated score
    """
    return sum(item.value * multiplier for item in items)
```

#### Commit Messages
- Use conventional commits format
- Be descriptive but concise
- Reference issues when applicable

```
feat: add support for custom personas

Implements the ability to create and manage custom personas
beyond the built-in ones. Users can now define persona
behavior through YAML configuration files.

Closes #123
```

#### Testing
- Write tests for all new functionality
- Maintain >80% code coverage
- Use descriptive test names
- Include edge cases

```python
def test_calculate_score_with_empty_list():
    """Test score calculation with no items."""
    assert calculate_score([]) == 0.0

def test_calculate_score_with_multiplier():
    """Test score calculation with custom multiplier."""
    items = [Item(value=10), Item(value=20)]
    assert calculate_score(items, multiplier=2.0) == 60.0
```

## 🛠️ Development Workflow

### 1. Daily Development
```bash
# Start your day
git pull upstream main
git checkout -b feature/new-feature

# Make changes
# ... edit files ...

# Check your work
make dev  # Formats and runs all checks

# Commit
git add .
git commit -m "feat: add amazing feature"
```

### 2. Testing
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test
pytest tests/unit/test_config.py::TestConfig::test_load
```

### 3. Documentation
```bash
# Build docs
make docs

# Serve locally
make serve-docs
# Visit http://localhost:8000
```

## 🏆 Recognition

### Contributors
All contributors are recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Release notes
- Project documentation

### Becoming a Maintainer
Active contributors may be invited to become maintainers based on:
- Quality of contributions
- Consistency of involvement
- Understanding of project goals
- Community interaction

## 📞 Getting Help

### Resources
- [Documentation](docs/README.md)
- [Discord Community](https://discord.gg/superclaude)
- [GitHub Discussions](https://github.com/NUbem000/SuperClaude-Pro/discussions)

### Questions?
- Check existing issues
- Ask in Discord
- Create a discussion
- Email: contribute@superclaude.dev

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to SuperClaude Pro! 🎆**

Your efforts help make Claude Code more powerful for everyone.