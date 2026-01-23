# PolyMorph Testing

This directory contains tests for the PolyMorph Linux distribution build system.

## Test Structure

```
tests/
├── test_validation.py       # Unit tests for configuration validation
├── integration/             # Integration tests
│   └── test_build.sh       # Build process integration tests
└── README.md               # This file
```

## Running Tests

### Unit Tests

Run validation unit tests:

```bash
# Simple runner (no dependencies)
python3 tests/test_validation.py

# With pytest (if installed)
python3 -m pytest tests/test_validation.py -v
```

### Integration Tests

Run full integration test suite:

```bash
bash tests/integration/test_build.sh
```

This tests:
- Directory structure
- Required files presence
- Script syntax validation
- Manifest generation
- Configuration validation

### Quick Test (All)

Run all tests at once:

```bash
# Unit tests
python3 tests/test_validation.py

# Integration tests
bash tests/integration/test_build.sh
```

## Test Coverage

### Unit Tests (`test_validation.py`)

- **Basic Validation**: Tests valid and invalid configurations
  - Valid Arch + KDE configuration
  - Invalid combinations (GNOME + OpenRC, i3 + Wayland)
  - Experimental base warnings
  - Missing required fields

- **Presets**: Validates all built-in presets
  - Ensures all presets are valid
  - Tests preset loading functionality

- **Filesystem Validation**: Filesystem-specific rules
  - ZFS on unsupported kernels
  - Filesystem package requirements

### Integration Tests (`test_build.sh`)

- **Project Structure**: Validates directory layout
- **Required Files**: Checks all necessary files exist
- **Script Syntax**: Python syntax validation
- **Manifest Generation**: Tests netinstall.yaml creation
- **Configuration Validation**: Tests validator with real configs

## Adding New Tests

### Unit Tests

Add new test methods to `test_validation.py`:

```python
def test_your_feature(self):
    """Test description."""
    validator = load_test_validator()
    config = {
        'base': 'arch',
        # ... your config
    }
    
    result = validator.validate_config(config)
    assert result.is_valid, "Should be valid"
```

### Integration Tests

Add new test functions to `test_build.sh`:

```bash
test_your_feature() {
    log_info "Testing your feature..."
    
    # Your test code here
    
    if [ condition ]; then
        log_success "Test passed"
        return 0
    else
        log_error "Test failed"
        return 1
    fi
}
```

Then add to the `TESTS` array in `main()`.

## Continuous Integration

These tests are designed to run in CI/CD pipelines. See `.github/workflows/` (when created) for CI configuration.

## Dependencies

### Required
- Python 3.6+
- PyYAML (`python3 -m pip install pyyaml`)
- Bash 4.0+

### Optional
- pytest (for enhanced test output)
- pytest-cov (for coverage reports)

Install optional dependencies:
```bash
python3 -m pip install pytest pytest-cov
```

## Test Data

Test configurations and matrices are loaded from:
- `config/compatibility-matrix.yaml` - Compatibility rules
- `manifests/*.yaml` - Package manifests

## Troubleshooting

**Import errors**: Make sure you're running from the project root:
```bash
cd /path/to/linux-distro
python3 tests/test_validation.py
```

**Matrix not found**: Ensure `config/compatibility-matrix.yaml` exists:
```bash
ls -l config/compatibility-matrix.yaml
```

**Permission denied**: Make scripts executable:
```bash
chmod +x tests/integration/*.sh
```
