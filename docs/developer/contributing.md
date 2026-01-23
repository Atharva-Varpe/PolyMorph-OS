# Contributing to PolyMorph

Thank you for considering contributing to PolyMorph! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

- **Report bugs** - Found an issue? Let us know!
- **Suggest features** - Have an idea? We'd love to hear it!
- **Fix bugs** - Check our issue tracker
- **Add features** - Implement new functionality
- **Improve docs** - Documentation is always welcome
- **Write tests** - Help us maintain quality
- **Package manifests** - Add or update package definitions

## 🚀 Getting Started

### Prerequisites

- Git knowledge
- Python 3.6+
- Arch Linux (for testing builds)
- Basic understanding of Linux systems

### Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/polymorph.git
cd polymorph

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/polymorph.git
```

### Set Up Development Environment

```bash
# Install dependencies
sudo pacman -S --needed archiso python python-yaml

# Install Python development dependencies (optional)
python3 -m pip install --user pytest pytest-cov black flake8

# Make scripts executable
chmod +x scripts/*.py tests/**/*.sh
```

### Run Tests

```bash
# Unit tests
python3 tests/test_validation.py

# Integration tests
bash tests/integration/test_build.sh

# Test a specific preset
python3 scripts/validate_config.py --preset desktop
```

## 📝 Development Workflow

### 1. Create a Branch

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

Follow our coding standards:

**Python:**
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions/classes
- Keep functions focused and small

**Bash:**
- Use `#!/bin/bash` shebang
- Enable strict mode: `set -euo pipefail`
- Quote variables: `"$var"`
- Use meaningful function names

**YAML:**
- Use 2-space indentation
- Add comments for complex sections
- Validate syntax before committing

### 3. Test Your Changes

```bash
# Run validation tests
python3 tests/test_validation.py

# Test manifest generation
python3 scripts/generate_netinstall.py

# Validate compatibility matrix
python3 scripts/validate_config.py --preset desktop

# For build changes, test ISO creation
./build.sh
```

### 4. Commit Changes

Write clear, descriptive commit messages:

```bash
git add .
git commit -m "Add feature: Brief description

Longer description of what changed and why.
Fixes #123"
```

**Commit message format:**
```
Type: Short summary (50 chars or less)

Longer explanation if needed (wrap at 72 chars).
- Bullet points are okay
- Use present tense: "Add feature" not "Added feature"

Closes #issue_number
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Build/tooling changes

### 5. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# - Fill out the PR template
# - Link related issues
# - Request review
```

## 🏗️ Project Structure

```
polymorph/
├── build.sh                  # Main build script
├── iso/                      # archiso profile
│   ├── packages.x86_64      # Live ISO packages
│   ├── profiledef.sh        # ISO metadata
│   └── airootfs/            # Live ISO filesystem
├── calamares/               # Installer configuration
│   ├── settings.conf        # Main config
│   ├── modules/             # Module configs
│   └── branding/            # Visual branding
├── manifests/               # Package definitions
│   ├── base.yaml           # Base system options
│   ├── desktops.yaml       # Desktop environments
│   └── ...
├── scripts/                 # Build/validation scripts
│   ├── generate_netinstall.py
│   └── validate_config.py
├── config/                  # Configuration files
│   └── compatibility-matrix.yaml
├── tests/                   # Test suite
│   ├── test_validation.py
│   └── integration/
└── docs/                    # Documentation
    ├── user/
    ├── developer/
    └── README.md
```

## 📋 Contribution Guidelines

### Adding New Packages

To add packages to manifests:

1. **Edit appropriate manifest** in `manifests/`
2. **Follow YAML structure:**
   ```yaml
   package_category:
     package_name:
       packages: [pkg1, pkg2, pkg3]
       note: Brief description of what this installs
   ```
3. **Test manifest generation:**
   ```bash
   python3 scripts/generate_netinstall.py
   ```
4. **Validate compatibility** if adding restrictions

### Adding New Features

1. **Check existing issues** - Maybe it's already planned!
2. **Open an issue first** - Discuss the feature
3. **Get feedback** - Ensure it fits project goals
4. **Implement** - Follow development workflow
5. **Add tests** - Maintain test coverage
6. **Update docs** - Document new functionality

### Fixing Bugs

1. **Reproduce the bug** - Ensure you can replicate it
2. **Write a test** - That fails with the bug
3. **Fix the bug** - Make the test pass
4. **Verify** - Run full test suite
5. **Document** - Update changelog/docs

### Updating Compatibility Matrix

1. **Edit** `config/compatibility-matrix.yaml`
2. **Add test case** in `tests/test_validation.py`
3. **Verify validation:**
   ```bash
   python3 scripts/validate_config.py --preset YOUR_PRESET
   ```
4. **Update** `docs/compatibility-matrix.md`

### Documentation

Documentation improvements are always welcome!

- **User docs** - Simplify complex concepts
- **Developer docs** - Explain architecture
- **Examples** - Add practical examples
- **Troubleshooting** - Document solutions

### Code Review Process

All contributions require review:

1. **Automated checks** run on PR
   - Syntax validation
   - Test suite
   - Compatibility checks

2. **Human review** by maintainers
   - Code quality
   - Design patterns
   - Documentation
   - Test coverage

3. **Feedback addressed** - Make requested changes

4. **Approval and merge** - Once approved, we'll merge!

## 🧪 Testing Guidelines

### Unit Tests

Add tests for new validation logic:

```python
def test_your_feature(self):
    """Test description."""
    validator = load_test_validator()
    config = {'base': 'arch', ...}
    
    result = validator.validate_config(config)
    assert result.is_valid, "Should be valid"
```

### Integration Tests

Add to `tests/integration/test_build.sh`:

```bash
test_your_feature() {
    log_info "Testing your feature..."
    # Test code here
    if [ condition ]; then
        log_success "Test passed"
        return 0
    else
        log_error "Test failed"
        return 1
    fi
}
```

### Manual Testing

Before submitting PR, test:

1. **Build ISO** - Ensure it builds successfully
2. **Boot in QEMU** - Test live environment
3. **Install** - Complete installation process
4. **Boot installed system** - Verify it works

## 📜 Code of Conduct

- **Be respectful** - Treat others with kindness
- **Be constructive** - Provide helpful feedback
- **Be patient** - Everyone is learning
- **Be inclusive** - Welcome diverse perspectives

## 🐛 Reporting Bugs

Use our issue template and include:

- **Description** - What happened?
- **Expected behavior** - What should happen?
- **Steps to reproduce** - How to replicate?
- **Environment** - System details
- **Logs** - Relevant error messages
- **Screenshots** - If applicable

## 💡 Suggesting Features

Open an issue with:

- **Use case** - Why is this needed?
- **Description** - What should it do?
- **Alternatives** - Other solutions considered?
- **Impact** - Who benefits?

## 🏆 Recognition

Contributors are recognized in:

- **CONTRIBUTORS.md** - Hall of fame
- **Release notes** - Feature credits
- **Documentation** - Author attribution

## 📞 Getting Help

Stuck? Need guidance?

- **Discord/Matrix** - Real-time chat
- **GitHub Discussions** - Q&A forum
- **Issue tracker** - Specific questions
- **Email maintainers** - For sensitive issues

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

---

**Thank you for making PolyMorph better! 🎉**
