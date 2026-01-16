#!/usr/bin/env python3
"""
Generate Calamares netinstall.yaml from manifest files.
Reads YAML manifests from manifests/ and outputs netinstall.yaml for Calamares.
"""

import sys
import re
from pathlib import Path

def parse_simple_yaml(content):
    """Simple YAML parser for our manifest files."""
    result = {}
    current_key = None
    current_dict = None
    indent_level = 0
    
    for line in content.split('\n'):
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue
            
        # Calculate indent
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        
        # Key-value pair
        if ':' in stripped:
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()
            
            if indent == 0:
                current_key = key
                if value:
                    result[key] = value
                else:
                    result[key] = {}
                    current_dict = result[key]
            elif indent == 2 and current_dict is not None:
                if value:
                    # Parse value
                    if value.startswith('{') and value.endswith('}'):
                        # Parse inline dict {packages: [...]}
                        obj = {}
                        value = value[1:-1]  # Remove braces
                        for part in value.split(','):
                            if ':' in part:
                                k, v = part.split(':', 1)
                                k = k.strip()
                                v = v.strip()
                                if v.startswith('[') and v.endswith(']'):
                                    # Parse list
                                    v = v[1:-1]
                                    obj[k] = [item.strip() for item in v.split(',')]
                                else:
                                    obj[k] = v
                        current_dict[key] = obj
                    elif value.startswith('[') and value.endswith(']'):
                        # Parse list
                        value = value[1:-1]
                        current_dict[key] = [item.strip() for item in value.split(',')]
                    else:
                        current_dict[key] = value
                else:
                    current_dict[key] = {}
    
    return result

def load_manifests(manifests_dir):
    """Load all YAML manifests from the manifests directory."""
    manifests = {}
    for yaml_file in Path(manifests_dir).glob("*.yaml"):
        with open(yaml_file, 'r') as f:
            data = parse_simple_yaml(f.read())
            manifests[yaml_file.stem] = data
    return manifests

def create_netinstall_group(name, items, selected=False, critical=False, immutable=False, expanded=False):
    """Create a netinstall group structure."""
    group = {
        "name": name,
        "description": f"Choose {name.lower()} components",
        "selected": selected,
        "critical": critical,
        "immutable": immutable,
        "expanded": expanded,
        "packages": []
    }
    
    # Add subgroups
    subgroups = []
    for key, value in items.items():
        if isinstance(value, dict) and 'packages' in value:
            subgroup = {
                "name": key.replace('_', ' ').replace('-', ' ').title(),
                "description": value.get('note', f"{key} packages"),
                "selected": False,
                "critical": False,
                "packages": value['packages']
            }
            subgroups.append(subgroup)
    
    if subgroups:
        group["subgroups"] = subgroups
    
    return group

def generate_netinstall(manifests):
    """Generate netinstall configuration from manifests."""
    groups = []
    
    # Core System (immutable, required)
    if 'base' in manifests and 'arch' in manifests['base'].get('base_targets', {}):
        core_packages = manifests['base']['base_targets']['arch'].get('packages', [])
        core_packages.extend(['base-devel', 'linux-firmware', 'intel-ucode', 'amd-ucode', 'sudo', 'nano', 'vim'])
        groups.append({
            "name": "Core System",
            "description": "Base system packages (required)",
            "selected": True,
            "critical": True,
            "immutable": True,
            "expanded": False,
            "packages": list(set(core_packages))
        })
    
    # Bootloader (required)
    groups.append({
        "name": "Bootloader",
        "description": "GRUB bootloader (required)",
        "selected": True,
        "critical": True,
        "immutable": False,
        "expanded": False,
        "packages": ["grub", "efibootmgr", "os-prober", "dosfstools", "mtools"]
    })
    
    # Kernels
    if 'kernels' in manifests:
        groups.append(create_netinstall_group("Kernels", manifests['kernels'], selected=True, expanded=True))
    
    # Desktop Environments
    if 'desktops' in manifests:
        groups.append(create_netinstall_group("Desktop Environments", manifests['desktops'], selected=False, expanded=True))
    
    # Display Server
    if 'display' in manifests:
        groups.append(create_netinstall_group("Display Server", manifests['display'], selected=True, expanded=False))
    
    # Init Systems
    if 'init' in manifests:
        init_group = create_netinstall_group("Init System", manifests['init'].get('init_systems', {}), selected=True, expanded=False)
        # Systemd selected by default
        if 'subgroups' in init_group:
            for sg in init_group['subgroups']:
                if 'Systemd' in sg['name']:
                    sg['selected'] = True
        groups.append(init_group)
    
    # Filesystems
    if 'filesystems' in manifests:
        groups.append(create_netinstall_group("Filesystem Tools", manifests['filesystems'], selected=True, expanded=False))
    
    # Network
    if 'network' in manifests:
        net_group = create_netinstall_group("Network Manager", manifests['network'], selected=True, expanded=False)
        # NetworkManager selected by default
        if 'subgroups' in net_group:
            for sg in net_group['subgroups']:
                if 'Networkmanager' in sg['name']:
                    sg['selected'] = True
        groups.append(net_group)
    
    # Audio
    if 'audio' in manifests:
        audio_group = create_netinstall_group("Audio Server", manifests['audio'], selected=True, expanded=False)
        # PipeWire selected by default
        if 'subgroups' in audio_group:
            for sg in audio_group['subgroups']:
                if 'Pipewire' in sg['name']:
                    sg['selected'] = True
        groups.append(audio_group)
    
    # Graphics Drivers
    if 'drivers' in manifests:
        groups.append(create_netinstall_group("Graphics Drivers", manifests['drivers'], selected=True, expanded=True))
    
    # Virtualization
    if 'virtualization' in manifests:
        groups.append(create_netinstall_group("Virtualization", manifests['virtualization'], selected=False, expanded=False))
    
    return groups

def write_yaml(data, f, indent=0):
    """Simple YAML writer for our netinstall config."""
    spaces = "  " * indent
    
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                f.write(f"{spaces}- ")
                first = True
                for key, value in item.items():
                    if first:
                        f.write(f"{key}: ")
                        first = False
                    else:
                        f.write(f"{spaces}  {key}: ")
                    
                    if isinstance(value, bool):
                        f.write(f"{str(value).lower()}\n")
                    elif isinstance(value, list):
                        if not value:
                            f.write("[]\n")
                        else:
                            f.write("\n")
                            for v in value:
                                f.write(f"{spaces}    - {v}\n")
                    elif isinstance(value, dict):
                        f.write("\n")
                        write_yaml([value], f, indent + 2)
                    else:
                        f.write(f"{value}\n")
            else:
                f.write(f"{spaces}- {item}\n")
    elif isinstance(data, dict):
        for key, value in data.items():
            f.write(f"{spaces}{key}: ")
            if isinstance(value, bool):
                f.write(f"{str(value).lower()}\n")
            elif isinstance(value, list):
                f.write("\n")
                write_yaml(value, f, indent + 1)
            elif isinstance(value, dict):
                f.write("\n")
                write_yaml(value, f, indent + 1)
            else:
                f.write(f"{value}\n")

def main():
    script_dir = Path(__file__).parent.parent
    manifests_dir = script_dir / "manifests"
    output_file = script_dir / "calamares" / "modules" / "netinstall.yaml"
    
    print(f"Loading manifests from {manifests_dir}...")
    manifests = load_manifests(manifests_dir)
    
    print(f"Generating netinstall configuration...")
    groups = generate_netinstall(manifests)
    
    print(f"Writing to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("---\n")
        f.write("# PolyMorph Netinstall Configuration\n")
        f.write("# Auto-generated from manifests/ - DO NOT EDIT MANUALLY\n")
        f.write("# Run: scripts/generate_netinstall.py to regenerate\n\n")
        write_yaml(groups, f)
    
    print(f"✓ Generated {output_file}")
    print(f"  Groups: {len(groups)}")

if __name__ == "__main__":
    main()
