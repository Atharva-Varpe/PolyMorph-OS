#!/usr/bin/env python3
"""
Unit tests for configuration validation.
Run with: python3 -m pytest tests/
or: python3 tests/test_validation.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.validate_config import ConfigValidator, ValidationResult


def load_test_validator():
    """Load validator with test matrix."""
    matrix_path = Path(__file__).parent.parent / "config" / "compatibility-matrix.yaml"
    return ConfigValidator(matrix_path)


class TestBasicValidation:
    """Test basic validation functionality."""
    
    def test_valid_arch_kde_config(self):
        """Test a valid Arch + KDE configuration."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'systemd',
            'desktop': 'plasma-kde',
            'display_server': 'wayland',
            'kernel': 'linux',
            'filesystem': 'ext4'
        }
        
        result = validator.validate_config(config)
        assert result.is_valid, f"Should be valid but got errors: {result.errors}"
        assert len(result.errors) == 0
    
    def test_invalid_gnome_openrc(self):
        """Test that GNOME with OpenRC is rejected."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'openrc',
            'desktop': 'gnome',
            'display_server': 'wayland'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "GNOME + OpenRC should be invalid"
        assert any('systemd' in err.lower() for err in result.errors)
    
    def test_invalid_i3_wayland(self):
        """Test that i3 with Wayland is rejected."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'systemd',
            'wm': 'i3',
            'display_server': 'wayland'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "i3 + Wayland should be invalid"
    
    def test_experimental_base_warning(self):
        """Test that experimental bases generate warnings."""
        validator = load_test_validator()
        config = {
            'base': 'debian',
            'init': 'systemd',
            'kernel': 'linux'
        }
        
        result = validator.validate_config(config)
        assert len(result.warnings) > 0, "Should have warnings for experimental base"
        assert any('experimental' in warn.lower() for warn in result.warnings)
    
    def test_missing_base(self):
        """Test that missing base is rejected."""
        validator = load_test_validator()
        config = {
            'init': 'systemd',
            'desktop': 'plasma-kde'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Missing base should be invalid"
    
    def test_void_only_runit(self):
        """Test that Void Linux only accepts runit."""
        validator = load_test_validator()
        config = {
            'base': 'void',
            'init': 'systemd'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Void + systemd should be invalid"


class TestPresets:
    """Test preset configurations."""
    
    def test_all_presets_valid(self):
        """Test that all built-in presets are valid."""
        validator = load_test_validator()
        presets = validator.list_presets()
        
        for preset_name, _ in presets:
            config = validator.get_preset(preset_name)
            result = validator.validate_config(config)
            assert result.is_valid, f"Preset '{preset_name}' should be valid but got: {result.errors}"
    
    def test_preset_loading(self):
        """Test preset loading."""
        validator = load_test_validator()
        desktop_preset = validator.get_preset('desktop')
        
        assert desktop_preset is not None
        assert desktop_preset.get('base') == 'arch'
        assert desktop_preset.get('desktop') == 'plasma-kde'


class TestFileSystemValidation:
    """Test filesystem-specific validation."""
    
    def test_zfs_kernel_warning(self):
        """Test that ZFS on zen kernel generates warning."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'systemd',
            'kernel': 'linux-zen',
            'filesystem': 'zfs'
        }
        
        result = validator.validate_config(config)
        # Should have a warning about ZFS on zen kernel
        assert len(result.warnings) > 0 or len(result.errors) > 0


def run_simple_tests():
    """Run tests without pytest."""
    print("Running validation tests...\n")
    
    test_classes = [TestBasicValidation(), TestPresets(), TestFileSystemValidation()]
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"Testing {class_name}:")
        
        # Get all test methods
        test_methods = [m for m in dir(test_class) if m.startswith('test_')]
        
        for method_name in test_methods:
            total_tests += 1
            method = getattr(test_class, method_name)
            
            try:
                method()
                print(f"  ✓ {method_name}")
                passed_tests += 1
            except AssertionError as e:
                print(f"  ✗ {method_name}: {e}")
                failed_tests.append((class_name, method_name, str(e)))
            except Exception as e:
                print(f"  ✗ {method_name}: Unexpected error: {e}")
                failed_tests.append((class_name, method_name, f"Unexpected: {e}"))
        
        print()
    
    # Summary
    print("=" * 60)
    print(f"Tests: {passed_tests}/{total_tests} passed")
    
    if failed_tests:
        print(f"\nFailed tests:")
        for class_name, method_name, error in failed_tests:
            print(f"  • {class_name}.{method_name}")
            print(f"    {error}")
        return 1
    else:
        print("\n✅ All tests passed!")
        return 0


if __name__ == '__main__':
    sys.exit(run_simple_tests())
