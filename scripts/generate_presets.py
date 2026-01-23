#!/usr/bin/env python3
"""
Generate preset selector module for Calamares.
Creates a custom module that allows users to quickly select pre-configured presets.
"""

import sys
import yaml
from pathlib import Path


def load_compatibility_matrix(matrix_path):
    """Load the compatibility matrix."""
    with open(matrix_path, 'r') as f:
        return yaml.safe_load(f)


def generate_preset_module(matrix, output_path):
    """Generate preset configuration for Calamares."""
    presets = matrix.get('presets', {})
    
    # Create preset groups for netinstall
    preset_groups = []
    
    for preset_id, preset_data in presets.items():
        group = {
            'name': preset_data.get('name', preset_id.title()),
            'description': preset_data.get('description', ''),
            'selected': False,
            'critical': False,
            'hidden': False,
            'packages': [],
            'subgroups': []
        }
        
        # Add metadata as description
        details = []
        if 'base' in preset_data:
            details.append(f"Base: {preset_data['base']}")
        if 'desktop' in preset_data:
            details.append(f"Desktop: {preset_data['desktop']}")
        elif 'wm' in preset_data:
            details.append(f"WM: {preset_data['wm']}")
        if 'init' in preset_data:
            details.append(f"Init: {preset_data['init']}")
        if 'kernel' in preset_data:
            details.append(f"Kernel: {preset_data['kernel']}")
        
        # Add size and time estimates
        if 'estimated_size_mb' in preset_data:
            size_gb = preset_data['estimated_size_mb'] / 1024
            details.append(f"~{size_gb:.1f}GB")
        if 'estimated_time_min' in preset_data:
            details.append(f"~{preset_data['estimated_time_min']}min install")
        
        group['description'] = f"{group['description']}\n{' | '.join(details)}"
        
        preset_groups.append(group)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write("---\n")
        f.write("# PolyMorph Quick Start Presets\n")
        f.write("# Auto-generated - Select one of these presets for quick installation\n\n")
        yaml.dump(preset_groups, f, default_flow_style=False, sort_keys=False)
    
    return len(preset_groups)


def main():
    script_dir = Path(__file__).parent.parent
    matrix_path = script_dir / "config" / "compatibility-matrix.yaml"
    output_path = script_dir / "calamares" / "modules" / "presets.yaml"
    
    if not matrix_path.exists():
        print(f"❌ Compatibility matrix not found: {matrix_path}", file=sys.stderr)
        return 1
    
    print("Loading compatibility matrix...")
    matrix = load_compatibility_matrix(matrix_path)
    
    print("Generating preset module...")
    count = generate_preset_module(matrix, output_path)
    
    print(f"✓ Generated {count} presets in {output_path}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
