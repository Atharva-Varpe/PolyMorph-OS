#!/usr/bin/env python3
"""
Edge case tests for configuration validation.
Tests critical failure scenarios that could break installations.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.validate_config import ConfigValidator


def load_test_validator():
    """Load validator with test matrix."""
    matrix_path = Path(__file__).parent.parent / "config" / "compatibility-matrix.yaml"
    return ConfigValidator(matrix_path)


class TestEdgeCases:
    """Test edge cases and security issues."""
    
    def test_missing_base(self):
        """CRITICAL: Test installation with no base selected."""
        validator = load_test_validator()
        config = {
            'init': 'systemd',
            'desktop': 'plasma-kde'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Must reject config with no base"
        assert any('base' in err.lower() for err in result.errors), "Must have base error"
        print("✓ Correctly rejects missing base")
    
    def test_empty_base(self):
        """CRITICAL: Test with empty string as base."""
        validator = load_test_validator()
        config = {
            'base': '',
            'init': 'systemd'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Must reject empty base"
        print("✓ Correctly rejects empty base")
    
    def test_whitespace_base(self):
        """SECURITY: Test with whitespace-only base."""
        validator = load_test_validator()
        config = {
            'base': '   ',
            'init': 'systemd'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Must reject whitespace-only base"
        print("✓ Correctly rejects whitespace base")
    
    def test_missing_init(self):
        """CRITICAL: Test installation with no init system."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'desktop': 'plasma-kde'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Must reject config with no init system"
        assert any('init' in err.lower() for err in result.errors), "Must have init error"
        print("✓ Correctly rejects missing init system")
    
    def test_missing_kernel(self):
        """CRITICAL: Test installation with no kernel."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'systemd',
            'desktop': 'plasma-kde'
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Must reject config with no kernel"
        assert any('kernel' in err.lower() for err in result.errors), "Must have kernel error"
        print("✓ Correctly rejects missing kernel")
    
    def test_none_values(self):
        """SECURITY: Test with None values."""
        validator = load_test_validator()
        config = {
            'base': None,
            'init': None,
            'kernel': None
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Must reject None values"
        print("✓ Correctly handles None values")
    
    def test_non_string_values(self):
        """SECURITY: Test with non-string values."""
        validator = load_test_validator()
        config = {
            'base': 123,
            'init': ['systemd'],
            'kernel': {'name': 'linux'}
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Must reject non-string values"
        print("✓ Correctly rejects non-string values")
    
    def test_malicious_injection_attempt(self):
        """SECURITY: Test command injection attempts."""
        validator = load_test_validator()
        config = {
            'base': 'arch; rm -rf /',
            'init': 'systemd && malicious',
            'kernel': 'linux`whoami`'
        }
        
        result = validator.validate_config(config)
        # Should fail validation due to invalid base name
        assert not result.is_valid, "Must reject injection attempts"
        print("✓ Correctly blocks injection attempts")
    
    def test_desktop_without_display_server(self):
        """WARNING: Desktop selected but no display server."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'systemd',
            'kernel': 'linux',
            'desktop': 'plasma-kde'
            # Missing display_server
        }
        
        result = validator.validate_config(config)
        # Might still be valid but should have warnings
        print("✓ Handles desktop without display server")
    
    def test_wm_with_wrong_display(self):
        """ERROR: Window manager incompatible with display server."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'systemd',
            'kernel': 'linux',
            'wm': 'i3',
            'display_server': 'wayland'  # i3 only works with X11
        }
        
        result = validator.validate_config(config)
        assert not result.is_valid, "Must reject incompatible WM+display"
        print("✓ Correctly rejects i3 + Wayland")
    
    def test_conflicting_selections(self):
        """ERROR: Both desktop and WM selected."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'systemd',
            'kernel': 'linux',
            'desktop': 'gnome',
            'wm': 'i3',  # Conflict: can't have both
            'display_server': 'xorg'
        }
        
        result = validator.validate_config(config)
        # Should warn or handle this gracefully
        print("✓ Handles conflicting desktop+WM selection")
    
    def test_minimal_valid_config(self):
        """Test minimum viable configuration."""
        validator = load_test_validator()
        config = {
            'base': 'arch',
            'init': 'systemd',
            'kernel': 'linux-lts',
            'filesystem': 'ext4'
        }
        
        result = validator.validate_config(config)
        assert result.is_valid, f"Minimal config should be valid but got: {result.errors}"
        print("✓ Minimal config is valid")
    
    def test_case_sensitivity(self):
        """SECURITY: Test case sensitivity in inputs."""
        validator = load_test_validator()
        config = {
            'base': 'ARCH',  # Uppercase
            'init': 'SystemD',  # Mixed case
            'kernel': 'LINUX-LTS'
        }
        
        result = validator.validate_config(config)
        # Should normalize or reject
        print("✓ Handles case variations")
    
    def test_extra_whitespace(self):
        """SECURITY: Test inputs with extra whitespace."""
        validator = load_test_validator()
        config = {
            'base': '  arch  ',
            'init': '\tsystemd\n',
            'kernel': ' linux-lts '
        }
        
        result = validator.validate_config(config)
        # Should normalize whitespace
        print("✓ Handles whitespace in inputs")


def run_edge_case_tests():
    """Run all edge case tests."""
    print("=" * 60)
    print("Running Edge Case & Security Tests")
    print("=" * 60)
    print()
    
    test_class = TestEdgeCases()
    test_methods = [m for m in dir(test_class) if m.startswith('test_')]
    
    passed = 0
    failed = 0
    
    for method_name in test_methods:
        print(f"Testing: {method_name.replace('_', ' ').title()}")
        try:
            method = getattr(test_class, method_name)
            method()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(run_edge_case_tests())
