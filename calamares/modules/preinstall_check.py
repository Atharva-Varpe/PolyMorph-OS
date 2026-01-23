#!/usr/bin/env python3
"""
Pre-installation validation module for Calamares.
This would be integrated as a custom Calamares module to validate
configurations before allowing installation to proceed.

CRITICAL: This prevents installation with invalid configurations.
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple


def load_netinstall_selections(netinstall_file: Path) -> Dict:
    """Load user selections from netinstall module."""
    # This would be called by Calamares with actual user selections
    # For now, this is a template
    pass


def validate_required_selections(selections: Dict) -> Tuple[bool, List[str]]:
    """Validate that all required components are selected."""
    errors = []
    
    # Check for core system
    if not selections.get('core_system'):
        errors.append("CRITICAL: Core system packages must be selected")
    
    # Check for bootloader
    if not selections.get('bootloader'):
        errors.append("CRITICAL: Bootloader must be selected")
    
    # Check for at least one kernel
    if not selections.get('kernel'):
        errors.append("CRITICAL: At least one kernel must be selected")
    
    # Check for init system
    if not selections.get('init'):
        errors.append("CRITICAL: Init system must be selected")
    
    # If desktop selected, check for display server
    if selections.get('desktop') and not selections.get('display_server'):
        errors.append("WARNING: Desktop environment selected but no display server")
    
    return len(errors) == 0, errors


def validate_disk_space(selections: Dict, available_space_mb: int) -> Tuple[bool, List[str]]:
    """Validate sufficient disk space for selected components."""
    errors = []
    
    # Estimate based on selections
    required_space = 1500  # Base minimum
    
    if selections.get('desktop'):
        required_space += 5000
    elif selections.get('wm'):
        required_space += 2000
    
    if selections.get('development_tools'):
        required_space += 2000
    
    # Add 20% buffer
    required_space = int(required_space * 1.2)
    
    if available_space_mb < required_space:
        errors.append(
            f"Insufficient disk space: {available_space_mb}MB available, "
            f"{required_space}MB required"
        )
    
    return len(errors) == 0, errors


def main():
    """Example validation flow."""
    print("Pre-installation validation module")
    print("This would be integrated into Calamares")
    
    # Example: validate required components
    test_selections = {
        'core_system': True,
        'bootloader': True,
        'kernel': 'linux-lts',
        'init': 'systemd',
        'desktop': 'plasma-kde',
        'display_server': 'wayland'
    }
    
    valid, errors = validate_required_selections(test_selections)
    
    if valid:
        print("✓ Required selections validated")
    else:
        print("✗ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
