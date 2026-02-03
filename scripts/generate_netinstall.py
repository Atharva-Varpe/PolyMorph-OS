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
    """Generate unified netinstall configuration with all distributions."""
    groups = []
    
    # Base Distribution Selector (CRITICAL - User chooses which OS to install)
    # This is the FIRST and MOST IMPORTANT choice - determines target OS
    if 'base' in manifests and 'base_targets' in manifests['base']:
        base_subgroups = []
        for distro, config in manifests['base']['base_targets'].items():
            note = config.get('note', f'{distro.title()} base system')
            
            # Mark with special identifier so Calamares module knows which bootstrap to use
            base_subgroups.append({
                "name": distro.title(),
                "description": note,
                "selected": (distro == 'arch'),  # Arch selected by default
                "critical": False,
                "packages": [f"__POLYMORPH_BASE__{distro.upper()}__"]  # Marker for custom module
            })
        
        groups.append({
            "name": "Base Distribution",
            "description": "Choose which Linux distribution to install (SELECT EXACTLY ONE)",
            "selected": True,
            "critical": True,
            "immutable": False,
            "expanded": True,
            "packages": [],
            "subgroups": base_subgroups
        })
    
    # Core System Packages (Common to all - installed via bootstrap)
    # NOTE: These packages are NOT installed to target system
    # They're available in the live environment for bootstrapping
    groups.append({
        "name": "Core System",
        "description": "Essential system packages (automatically included)",
        "selected": True,
        "critical": True,
        "immutable": True,
        "expanded": False,
        "packages": []  # Empty - base system comes from bootstrap process
    })
    
    # Bootloader (required for all distributions)
    groups.append({
        "name": "Bootloader",
        "description": "GRUB bootloader (required)",
        "selected": True,
        "critical": True,
        "immutable": False,
        "expanded": False,
        "packages": ["grub", "efibootmgr", "os-prober"]
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
    
    print(f"[INFO] Loading manifests from {manifests_dir}...")
    manifests = load_manifests(manifests_dir)
    
    print(f"[INFO] Generating unified multi-distro netinstall configuration...")
    groups = generate_netinstall(manifests)
    
    print(f"[INFO] Writing to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        f.write("# PolyMorph OS - Unified Multi-Distribution Installer\n")
        f.write("# \n")
        f.write("# ONE ISO - ANY DISTRIBUTION\n")
        f.write("# \n")
        f.write("# Architecture:\n")
        f.write("#   - Live Environment: Arch Linux (provides bootstrap tools)\n")
        f.write("#   - Target Installation: User's choice (Arch, Debian, Ubuntu, etc.)\n")
        f.write("# \n")
        f.write("# How it works:\n")
        f.write("#   1. User boots Arch-based live ISO\n")
        f.write("#   2. Calamares installer loads this configuration\n")
        f.write("#   3. User selects BASE DISTRIBUTION (which OS to install)\n")
        f.write("#   4. User selects packages compatible with chosen distro\n")
        f.write("#   5. Custom module bootstraps selected distro to disk\n")
        f.write("# \n")
        f.write("# Auto-generated from manifests - DO NOT EDIT MANUALLY\n")
        f.write("# \n\n")
        write_yaml(groups, f)
    
    print(f"[PASS] Generated netinstall configuration")
    print(f"       Output: {output_file}")
    print(f"       Groups: {len(groups)}")
    print(f"       Architecture: ONE ISO → ANY DISTRO")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

