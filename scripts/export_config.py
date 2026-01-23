#!/usr/bin/env python3
"""
Export installation configuration to a shareable YAML file.
This allows users to save their installation choices for:
- Documentation purposes
- Reproducing installations
- Sharing configurations
- Community troubleshooting
"""

import sys
import yaml
from datetime import datetime
from pathlib import Path


def export_configuration(config, metadata=None):
    """Export configuration with metadata."""
    export_data = {
        'polymorph_config': {
            'version': '1.0',
            'generated': datetime.now().isoformat(),
            'metadata': metadata or {},
            'configuration': config
        }
    }
    return export_data


def generate_summary_text(config, metadata=None):
    """Generate human-readable summary."""
    lines = [
        "=" * 60,
        "PolyMorph Installation Configuration",
        "=" * 60,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ]
    
    if metadata:
        lines.append("Installation Metadata:")
        for key, value in metadata.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
    
    lines.append("Configuration:")
    
    # Group by category
    categories = {
        'System': ['base', 'init', 'kernel', 'filesystem'],
        'Desktop': ['desktop', 'wm', 'display_server'],
        'Hardware': ['graphics', 'audio'],
        'Network': ['network'],
        'Other': []
    }
    
    for category, keys in categories.items():
        category_items = [(k, config.get(k)) for k in keys if k in config]
        if category_items:
            lines.append(f"\n{category}:")
            for key, value in category_items:
                lines.append(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Add any remaining items
    covered_keys = sum(categories.values(), [])
    other_items = [(k, v) for k, v in config.items() if k not in covered_keys]
    if other_items:
        lines.append(f"\nAdditional:")
        for key, value in other_items:
            lines.append(f"  {key.replace('_', ' ').title()}: {value}")
    
    lines.extend([
        "",
        "=" * 60,
        "To reproduce this installation:",
        f"  python3 scripts/validate_config.py --config <this_file>.yaml",
        "=" * 60
    ])
    
    return '\n'.join(lines)


def save_export(export_data, output_path, format='yaml'):
    """Save export to file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == 'yaml':
        with open(output_path, 'w') as f:
            yaml.dump(export_data, f, default_flow_style=False, sort_keys=False)
    elif format == 'txt':
        config = export_data['polymorph_config']['configuration']
        metadata = export_data['polymorph_config']['metadata']
        summary = generate_summary_text(config, metadata)
        with open(output_path, 'w') as f:
            f.write(summary)
    
    return output_path


def main():
    """Example usage and testing."""
    # Example configuration
    example_config = {
        'base': 'arch',
        'init': 'systemd',
        'kernel': 'linux-lts',
        'filesystem': 'btrfs',
        'desktop': 'plasma-kde',
        'display_server': 'wayland',
        'audio': 'pipewire',
        'network': 'networkmanager',
        'graphics': 'open-source'
    }
    
    example_metadata = {
        'hostname': 'polymorph-desktop',
        'username': 'user',
        'installation_date': datetime.now().strftime('%Y-%m-%d'),
        'iso_version': '0.1.0'
    }
    
    # Export
    export_data = export_configuration(example_config, example_metadata)
    
    # Save as YAML
    yaml_path = Path('/tmp/polymorph-config-example.yaml')
    save_export(export_data, yaml_path, format='yaml')
    print(f"✓ Exported YAML to: {yaml_path}")
    
    # Save as text summary
    txt_path = Path('/tmp/polymorph-config-example.txt')
    save_export(export_data, txt_path, format='txt')
    print(f"✓ Exported summary to: {txt_path}")
    
    # Print summary
    print("\n" + generate_summary_text(example_config, example_metadata))


if __name__ == '__main__':
    main()
