#!/usr/bin/env python3
"""PolyMorph Multi-Distribution Bootstrap Module for Calamares.

This module implements the "one ISO, many target distros" architecture by:
1) Reading the user's NetInstall selections from Calamares global storage.
2) Detecting the selected target base distribution via marker packages.
3) Bootstrapping the selected distro to the target root.
4) Installing the selected packages using the appropriate package manager.

Marker packages are injected by the generated NetInstall configuration:
  __POLYMORPH_BASE__ARCH__
  __POLYMORPH_BASE__DEBIAN__
  __POLYMORPH_BASE__UBUNTU__
  ...

Those markers are NOT real packages; this module filters them out of
Calamares package operations.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:
    import libcalamares  # type: ignore
except Exception:  # pragma: no cover
    libcalamares = None


MARKER_PREFIX = "__POLYMORPH_BASE__"
MARKER_SUFFIX = "__"
SUPPORTED_BASES = {"arch", "debian", "ubuntu"}


@dataclass(frozen=True)
class BootstrapConfig:
    debian_suite: str = "bookworm"
    debian_mirror: str = "http://deb.debian.org/debian"
    ubuntu_suite: str = "noble"
    ubuntu_mirror: str = "http://archive.ubuntu.com/ubuntu"
    debootstrap_arch: str = "amd64"


_PKG_NAME_RE = re.compile(r"^[a-zA-Z0-9._+-]+$")


def _extract_packages_from_package_operations(package_operations: Any) -> List[str]:
    """Extract a flat list of package names from Calamares `packageOperations`.

    `packageOperations` is a list of dicts (one per source module). Each dict may
    contain `install` and/or `try_install`, which are lists of either:
    - strings (plain package names)
    - dicts with at least a `package` field (for pre-/post-scripts)
    """
    if not package_operations:
        return []
    if not isinstance(package_operations, list):
        return []

    extracted: List[str] = []
    for op in package_operations:
        if not isinstance(op, dict):
            continue
        for key in ("install", "try_install"):
            values = op.get(key)
            if not isinstance(values, list):
                continue
            for entry in values:
                if isinstance(entry, str):
                    extracted.append(entry)
                elif isinstance(entry, dict):
                    pkg = entry.get("package")
                    if isinstance(pkg, str):
                        extracted.append(pkg)
    return extracted


def _detect_base_from_markers(packages: Sequence[str]) -> Optional[str]:
    markers: Set[str] = set()
    for p in packages:
        if p.startswith(MARKER_PREFIX) and p.endswith(MARKER_SUFFIX):
            markers.add(p)

    if not markers:
        return None
    if len(markers) > 1:
        raise ValueError(f"Multiple base distro markers selected: {sorted(markers)!r}")

    marker = next(iter(markers))
    token = marker[len(MARKER_PREFIX) : -len(MARKER_SUFFIX)]
    return token.lower()


def _filter_out_markers(packages: Sequence[str]) -> List[str]:
    return [p for p in packages if not (p.startswith(MARKER_PREFIX) and p.endswith(MARKER_SUFFIX))]


def _filter_package_operations_in_place(package_operations: Any) -> Any:
    """Remove marker packages from `packageOperations` (in-memory structure)."""
    if not isinstance(package_operations, list):
        return package_operations
    for op in package_operations:
        if not isinstance(op, dict):
            continue
        for key in ("install", "try_install"):
            values = op.get(key)
            if not isinstance(values, list):
                continue
            filtered: List[Any] = []
            for entry in values:
                if isinstance(entry, str):
                    if entry.startswith(MARKER_PREFIX) and entry.endswith(MARKER_SUFFIX):
                        continue
                    filtered.append(entry)
                elif isinstance(entry, dict):
                    pkg = entry.get("package")
                    if isinstance(pkg, str) and pkg.startswith(MARKER_PREFIX) and pkg.endswith(MARKER_SUFFIX):
                        continue
                    filtered.append(entry)
                else:
                    filtered.append(entry)
            op[key] = filtered
    return package_operations


def _validate_package_names(packages: Sequence[str]) -> List[str]:
    """Sanitize to safe package-name tokens only."""
    safe: List[str] = []
    for p in packages:
        if not isinstance(p, str):
            continue
        p = p.strip()
        if not p:
            continue
        if _PKG_NAME_RE.match(p):
            safe.append(p)
    return safe


def _get_config() -> BootstrapConfig:
    if libcalamares is None:  # pragma: no cover
        return BootstrapConfig()
    cfg = getattr(libcalamares.job, "configuration", None)
    if not isinstance(cfg, dict):
        return BootstrapConfig()
    debian = cfg.get("debian", {}) if isinstance(cfg.get("debian"), dict) else {}
    ubuntu = cfg.get("ubuntu", {}) if isinstance(cfg.get("ubuntu"), dict) else {}
    return BootstrapConfig(
        debian_suite=str(debian.get("suite", BootstrapConfig.debian_suite)),
        debian_mirror=str(debian.get("mirror", BootstrapConfig.debian_mirror)),
        ubuntu_suite=str(ubuntu.get("suite", BootstrapConfig.ubuntu_suite)),
        ubuntu_mirror=str(ubuntu.get("mirror", BootstrapConfig.ubuntu_mirror)),
        debootstrap_arch=str(cfg.get("debootstrapArch", BootstrapConfig.debootstrap_arch)),
    )


def get_selected_base_distribution_and_packages() -> Tuple[Optional[str], List[str]]:
    """Determine base distro and selected package list from Calamares global storage."""
    if libcalamares is None:  # pragma: no cover
        return None, []

    package_operations = libcalamares.globalstorage.value("packageOperations")
    selected = _extract_packages_from_package_operations(package_operations)
    base = _detect_base_from_markers(selected)

    # Remove marker packages from GS so later modules won't try to install them.
    filtered_ops = _filter_package_operations_in_place(package_operations)
    libcalamares.globalstorage.insert("packageOperations", filtered_ops)

    selected = _filter_out_markers(selected)
    selected = _validate_package_names(selected)
    return base, selected


def _run(cmd: Sequence[str]) -> None:
    subprocess.run(list(cmd), check=True)


def bootstrap_arch(root_mount_point: str, selected_packages: Sequence[str]) -> None:
    """Bootstrap Arch Linux using pacstrap, including selected packages."""
    if libcalamares is not None:
        libcalamares.utils.debug(f"Bootstrapping Arch Linux to {root_mount_point}")

    base_packages = ["base", "linux", "linux-firmware"]
    install_packages = list(dict.fromkeys(base_packages + list(selected_packages)))
    cmd = ["pacstrap", "-K", root_mount_point] + install_packages
    _run(cmd)


def _write_resolv_conf(root_mount_point: str) -> None:
    src = Path("/etc/resolv.conf")
    dst = Path(root_mount_point) / "etc" / "resolv.conf"
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            dst.write_bytes(src.read_bytes())
    except Exception:
        pass


def _chroot_cmd(root_mount_point: str, cmd: Sequence[str]) -> List[str]:
    return ["chroot", root_mount_point] + list(cmd)


def _apt_install(root_mount_point: str, packages: Sequence[str]) -> None:
    env = os.environ.copy()
    env["DEBIAN_FRONTEND"] = "noninteractive"
    _write_resolv_conf(root_mount_point)
    subprocess.run(_chroot_cmd(root_mount_point, ["apt-get", "update"]), check=True, env=env)
    subprocess.run(
        _chroot_cmd(root_mount_point, ["apt-get", "install", "-y", "--no-install-recommends"] + list(packages)),
        check=True,
        env=env,
    )


def bootstrap_debian_or_ubuntu(root_mount_point: str, selected_packages: Sequence[str], variant: str, cfg: BootstrapConfig) -> None:
    """Bootstrap Debian/Ubuntu with debootstrap and install minimal packages with apt."""
    if libcalamares is not None:
        libcalamares.utils.debug(f"Bootstrapping {variant} to {root_mount_point}")

    if variant == "debian":
        suite = cfg.debian_suite
        mirror = cfg.debian_mirror
        kernel_pkg = "linux-image-amd64"
    elif variant == "ubuntu":
        suite = cfg.ubuntu_suite
        mirror = cfg.ubuntu_mirror
        kernel_pkg = "linux-generic"
    else:
        raise ValueError(f"Unsupported variant {variant!r}")

    cmd = ["debootstrap", f"--arch={cfg.debootstrap_arch}", suite, root_mount_point, mirror]
    _run(cmd)

    # Minimal, bootable baseline. This deliberately ignores most Arch-named
    # package selections until a full cross-distro mapping layer is implemented.
    is_uefi = Path("/sys/firmware/efi").exists()
    grub_pkg = "grub-efi-amd64" if is_uefi else "grub-pc"

    baseline = [
        "sudo",
        "ca-certificates",
        "locales",
        "dbus",
        kernel_pkg,
        grub_pkg,
        "efibootmgr" if is_uefi else "",
        "os-prober",
        "network-manager",
    ]
    baseline = [p for p in baseline if p]
    _apt_install(root_mount_point, baseline)


def run():
    """
    Main entry point for Calamares module.
    This runs BEFORE the standard package installation.
    """
    if libcalamares is None:  # pragma: no cover
        raise RuntimeError("This module must be run inside Calamares")

    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")
    
    if not root_mount_point:
        libcalamares.utils.warning("No root mount point found!")
        return ("No root mount point", "Cannot proceed without target partition")
    
    libcalamares.utils.debug(f"Root mount point: {root_mount_point}")
    
    cfg = _get_config()

    # Determine which distribution was selected and gather selected packages
    try:
        base_distro, selected_packages = get_selected_base_distribution_and_packages()
    except Exception as e:
        return ("Invalid package selection", str(e))
    
    if not base_distro:
        # Netinstall is required and one option is preselected, so this is a safety net.
        base_distro = "arch"
    
    base_distro = base_distro.lower()
    libcalamares.utils.debug(f"Selected base distribution: {base_distro}")
    libcalamares.job.setprogress(0.1)
    
    try:
        if base_distro == "arch":
            libcalamares.job.setprogress(0.2)
            bootstrap_arch(root_mount_point, selected_packages)
            libcalamares.job.setprogress(0.9)
        elif base_distro == "debian":
            libcalamares.job.setprogress(0.2)
            bootstrap_debian_or_ubuntu(root_mount_point, selected_packages, "debian", cfg)
            libcalamares.job.setprogress(0.9)
        elif base_distro == "ubuntu":
            libcalamares.job.setprogress(0.2)
            bootstrap_debian_or_ubuntu(root_mount_point, selected_packages, "ubuntu", cfg)
            libcalamares.job.setprogress(0.9)
        else:
            return (
                f"Unsupported distribution: {base_distro}",
                f"Support for {base_distro} is not implemented. Supported: {', '.join(sorted(SUPPORTED_BASES))}.",
            )
    except FileNotFoundError as e:
        return ("Bootstrap tool missing", f"Required tool not found: {e}")
    except subprocess.CalledProcessError as e:
        return ("Bootstrap failed", f"Command failed: {e}")
    except Exception as e:
        return ("Bootstrap failed", str(e))
    
    libcalamares.job.setprogress(1.0)
    
    # Store the selected distro for other modules to use
    libcalamares.globalstorage.insert("polymorphBaseDistro", base_distro)
    
    return None  # Success
