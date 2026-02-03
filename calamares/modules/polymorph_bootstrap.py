#!/usr/bin/env python3
"""
PolyMorph Multi-Distribution Bootstrap Module for Calamares

This module detects which base distribution the user selected and
uses the appropriate bootstrap method to install it to the target disk.

Supported:
- Arch Linux: pacstrap
- Debian: debootstrap
- Ubuntu: debootstrap
- Others: Planned
"""

import libcalamares
import subprocess
import os
from pathlib import Path


def get_selected_base_distribution():
    """
    Parse netinstall selections to determine which base distro was chosen.
    Returns: ('arch'|'debian'|'ubuntu'|'fedora'|etc, selected_packages)
    """
    # Get netinstall module data
    netinstall_data = libcalamares.globalstorage.value("netinstallPackages")
    
    if not netinstall_data:
        return None, []
    
    # Look for Base Distribution group selection
    for group in netinstall_data:
        if group.get("name") == "Base Distribution":
            subgroups = group.get("subgroups", [])
            for subgroup in subgroups:
                if subgroup.get("selected", False):
                    distro_name = subgroup.get("name", "").lower()
                    packages = subgroup.get("packages", [])
                    return distro_name, packages
    
    # Default to Arch if nothing selected (shouldn't happen due to critical flag)
    return "arch", []


def bootstrap_arch(root_mount_point, packages):
    """Bootstrap Arch Linux using pacstrap."""
    libcalamares.utils.debug(f"Bootstrapping Arch Linux to {root_mount_point}")
    
    # Base packages for Arch
    base_packages = ["base", "linux", "linux-firmware"]
    
    # Run pacstrap
    cmd = ["pacstrap", root_mount_point] + base_packages
    
    try:
        subprocess.run(cmd, check=True)
        libcalamares.utils.debug("Arch bootstrap completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        libcalamares.utils.warning(f"Arch bootstrap failed: {e}")
        return False


def bootstrap_debian(root_mount_point, packages, variant="debian"):
    """Bootstrap Debian or Ubuntu using debootstrap."""
    libcalamares.utils.debug(f"Bootstrapping {variant.title()} to {root_mount_point}")
    
    # Determine suite/release
    if variant == "debian":
        suite = "stable"  # or bookworm, bullseye, etc.
        mirror = "http://deb.debian.org/debian"
    else:  # ubuntu
        suite = "jammy"  # or focal, mantic, etc.
        mirror = "http://archive.ubuntu.com/ubuntu"
    
    # Run debootstrap
    cmd = [
        "debootstrap",
        "--arch=amd64",
        suite,
        root_mount_point,
        mirror
    ]
    
    try:
        subprocess.run(cmd, check=True)
        libcalamares.utils.debug(f"{variant.title()} bootstrap completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        libcalamares.utils.warning(f"{variant.title()} bootstrap failed: {e}")
        return False


def run():
    """
    Main entry point for Calamares module.
    This runs BEFORE the standard package installation.
    """
    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")
    
    if not root_mount_point:
        libcalamares.utils.warning("No root mount point found!")
        return ("No root mount point", "Cannot proceed without target partition")
    
    libcalamares.utils.debug(f"Root mount point: {root_mount_point}")
    
    # Determine which distribution was selected
    base_distro, packages = get_selected_base_distribution()
    
    if not base_distro:
        return ("No distribution selected", 
                "Please select a base distribution in the package selection step")
    
    libcalamares.utils.debug(f"Selected base distribution: {base_distro}")
    libcalamares.job.setprogress(0.1)
    
    # Bootstrap the selected distribution
    success = False
    
    if base_distro == "arch":
        libcalamares.job.setprogress(0.2)
        success = bootstrap_arch(root_mount_point, packages)
        libcalamares.job.setprogress(0.9)
        
    elif base_distro == "debian":
        libcalamares.job.setprogress(0.2)
        success = bootstrap_debian(root_mount_point, packages, "debian")
        libcalamares.job.setprogress(0.9)
        
    elif base_distro == "ubuntu":
        libcalamares.job.setprogress(0.2)
        success = bootstrap_debian(root_mount_point, packages, "ubuntu")
        libcalamares.job.setprogress(0.9)
        
    else:
        return (f"Unsupported distribution: {base_distro}",
                f"Support for {base_distro} is not yet implemented. "
                f"Currently supported: Arch, Debian, Ubuntu")
    
    libcalamares.job.setprogress(1.0)
    
    if not success:
        return (f"Bootstrap failed for {base_distro}",
                f"Failed to install {base_distro} base system. Check logs for details.")
    
    # Store the selected distro for other modules to use
    libcalamares.globalstorage.insert("polymorphBaseDistro", base_distro)
    
    return None  # Success
