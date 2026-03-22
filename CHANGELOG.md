# PolyMorph Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - Fedora Support & Rices - 2026-03-22

### Added

**Fedora Base Support (Experimental)**
- Implemented `bootstrap_fedora()` in `polymorph_bootstrap.py` using `dnf --installroot`
- Bootstraps a minimal Fedora system: `fedora-release`, `kernel`, `systemd`, `grub2`,
  `NetworkManager`, UEFI or BIOS grub packages selected automatically
- Added `fedora_release` (default: `40`) and `fedora_mirror` config fields to `BootstrapConfig`
- Added `fedora:` section to `polymorph_bootstrap.conf` for release/mirror overrides
- Added `dnf` to `iso/packages.x86_64` so the live environment can run `dnf --installroot`
- Updated `SUPPORTED_BASES` to include `"fedora"`

**Premade Desktop Rice Installer (First-Boot Wizard)**
- New step 5 in `polymorph-first-boot`: interactive rice selection with six curated options:
  1. **DMS (DankMaterialShell)** — Full Wayland desktop shell, supports Arch/Fedora/Debian/Ubuntu/openSUSE/Gentoo via `dankinstall` one-liner ([github.com/AvengeMedia/DankMaterialShell](https://github.com/AvengeMedia/DankMaterialShell))
  2. **ML4W** — Feature-rich Hyprland dotfiles, supports Arch/Fedora/openSUSE ([github.com/mylinuxforwork/dotfiles](https://github.com/mylinuxforwork/dotfiles))
  3. **HyDE** — Aesthetic dynamic Hyprland dots with multi-theme switcher, Arch-based ([github.com/HyDE-Project/HyDE](https://github.com/HyDE-Project/HyDE))
  4. **Caelestia** — Hyprland + Quickshell rice, Arch only ([github.com/caelestia-dots/caelestia](https://github.com/caelestia-dots/caelestia))
  5. **JaKooLit Hyprland-Dots** — Multi-distro Hyprland configs ([github.com/JaKooLit/Hyprland-Dots](https://github.com/JaKooLit/Hyprland-Dots))
  6. **dots-hyprland (end-4)** — Usability-first Hyprland dotfiles ([github.com/end-4/dots-hyprland](https://github.com/end-4/dots-hyprland))
- Rices cloned to `~/.local/share/polymorph-rices/<name>` and updated on re-run
- **Dynamic distro-aware menu**: menu is built at runtime — only shows rices compatible with
  the installed distro; Arch-only rices (HyDE, Caelestia) are hidden on Fedora/Debian/Ubuntu
- Last option is always **"None — keep default DE configuration"** so users who want their
  selected DE without any rice overlay can skip cleanly

**Distro-Aware First-Boot Wizard**
- First-boot wizard now detects installed distro via `/etc/os-release`
- Package manager commands (update/install) automatically use `pacman`, `dnf`, or `apt`
  depending on the installed base distribution
- Package name mapping for distro-specific equivalents (e.g. `base-devel` → `@c-development`
  on Fedora, `build-essential` on Debian/Ubuntu)
- Caelestia rice install correctly warns and skips on non-Arch systems

### Changed
- Fedora status updated from "Planned" to "Experimental" in README and netinstall manifest
- ISO version bumped to `1.2.0` in `profiledef.sh` and `branding.desc`

### Fixed
- First-boot wizard `[1/4]` steps re-numbered to `[1/5]` to reflect the new rice step
- First-boot summary now records the installed distro ID

## [1.1.0] - ISO Release & Fixes - 2026-03-05

### Fixed

**Boot Branding**
- Replaced all "Arch Linux install medium" labels with "PolyMorph Linux" across
  GRUB (UEFI/BIOS), systemd-boot EFI entries, syslinux BIOS and PXE configs

**ISO Profile**
- Bumped `iso_version` from `0.1.0` to `1.1.0` in `profiledef.sh`
- Added `file_permissions` entries so `customize_airootfs.sh` and the first-boot
  script are marked executable inside the squashfs image

**Live Environment**
- `customize_airootfs.sh`: creates `polymorph` live user (password: polymorph),
  configures sudoers, sets hostname `polymorph-live`, runs `locale-gen`, and
  initialises the pacman keyring so in-installer package downloads succeed

**Package List**
- Added `pipewire`, `wireplumber`, `pipewire-pulse`, `pipewire-alsa` for audio
- Added `noto-fonts`, `noto-fonts-emoji` for font coverage
- Added `plasma-pa`, `breeze`, `breeze-gtk`, `kde-gtk-config`, `kscreen`,
  `xdg-desktop-portal-kde`, `xdg-user-dirs` for a fully functional KDE live session

**First-Boot Wizard**
- Complete rewrite of `polymorph-first-boot`; the previous version contained
  orphaned code fragments, mismatched if/fi blocks, and broken function bodies
  that would have caused the wizard to crash on launch

**Calamares Branding**
- Updated version strings to `1.1.0` in `branding.desc`

## [1.0.0] - Universal Multi-Distribution Installer - 2024

### Major Features

**ONE ISO → ANY DISTRO Architecture**
- Single universal ISO that can install any major Linux distribution
- User downloads once, chooses target distribution during installation
- Eliminates need for per-distribution ISO downloads

#### Multi-Distribution Support
- **Base Distribution Selector** in Calamares netinstall
  - Arch Linux (stable, full support)
  - Debian (experimental, Bookworm 12)
  - Ubuntu (experimental, Noble 24.04)
  - Fedora, openSUSE, Gentoo, Void, Alpine (planned)

- **Custom Bootstrap Module** (`polymorph_bootstrap.py`)
  - Detects selected base distribution from package markers
  - Calls appropriate bootstrap tool:
    - Arch: `pacstrap` (native)
    - Debian/Ubuntu: `debootstrap`
    - Fedora: `dnf --installroot` (planned)
    - openSUSE: `zypper --root` (planned)
  - Handles distribution-specific configuration

- **Bootstrap Tools in Live ISO**
  - `debootstrap` for Debian/Ubuntu
  - `debian-archive-keyring` and `ubuntu-keyring`
  - Future: Fedora, openSUSE tooling

#### Universal Package System
- **Manifest Format**: Arch package names used as universal identifiers
- **Cross-Distribution Translation**: Bootstrap module maps to target distro packages
- **Compatibility Matrix**: Validates combinations across all distributions
- **Distribution-Agnostic Components**: Kernels, desktops, drivers work with any base

### Architecture Changes
- Live ISO remains Arch-based (stability, tooling)
- Target system can be any supported distribution
- Calamares sequence updated: mount → bootstrap → packages → bootloader
- No squashfs unpacking - base system bootstrapped directly

## [0.2.0] - Security Hardening Release - 2024

### Security Fixes ⚠️ CRITICAL

This release fixes **12 critical security vulnerabilities** identified during comprehensive security audit.

#### CRITICAL Fixes
- **Added mandatory requirement for base distribution**
  - System will now reject installations without base packages
  - Prevents completely unbootable systems
  - Test: `test_edge_cases.py::test_missing_base`

- **Added mandatory requirement for init system**
  - System will now reject installations without init (systemd/runit/openrc)
  - Prevents kernel panic on boot
  - Test: `test_edge_cases.py::test_missing_init`

- **Added mandatory requirement for kernel**
  - System will now reject installations without kernel
  - Prevents unbootable systems
  - Test: `test_edge_cases.py::test_missing_kernel`

#### HIGH Priority Fixes
- **Fixed command injection vulnerability in package installation**
  - Added regex validation for package names: `^[a-zA-Z0-9._+-]+$`
  - Blocks injection attempts like: `vim; rm -rf /`
  - Test: `test_edge_cases.py::test_malicious_injection`

- **Fixed username injection vulnerability**
  - Added Linux-compliant username validation: `^[a-z_][a-z0-9_-]*[$]?$`
  - Prevents path traversal and command injection
  - Manual testing required

- **Prevented first-boot wizard from running as root**
  - Added EUID check at script start
  - Forces running as regular user with sudo when needed
  - Reduces privilege escalation risk

- **Created pre-installation validation module**
  - New `calamares/modules/preinstall_check.py`
  - Validates required components before installation
  - Checks disk space requirements
  - Prevents GUI bypassing validation

#### MEDIUM Priority Fixes
- **Added input type safety to validation**
  - Validates all config values are strings
  - Rejects None, integers, lists, dicts
  - Test: `test_edge_cases.py::test_non_string_values`

- **Added comprehensive logging to first-boot wizard**
  - All actions logged to `/var/log/polymorph-first-boot.log`
  - Timestamps for all operations
  - Error logging for debugging

- **Added error handling throughout first-boot wizard**
  - All sudo operations check return codes
  - Graceful failure with error messages
  - Prevents silent failures

#### LOW Priority Fixes
- **Secured PATH environment variable**
  - Set secure PATH at first-boot wizard start
  - Prevents PATH hijacking attacks

- **Fixed whitespace injection vulnerability**
  - All inputs stripped before validation
  - Prevents whitespace-only bypass
  - Test: `test_edge_cases.py::test_whitespace_base`

### Added
- **Comprehensive edge case test suite**
  - New `tests/test_edge_cases.py` with 14 tests
  - Tests all critical vulnerabilities
  - 100% pass rate

- **Security documentation**
  - New `SECURITY.md` - Complete security audit report
  - New `docs/SECURITY_AUDIT.md` - Summary and procedures
  - Vulnerability disclosure policy
  - Manual testing checklist

### Changed
- **Enhanced validation system**
  - `scripts/validate_config.py` - Added type checking and sanitization
  - All string inputs: strip, lowercase, validate type
  - Critical vs warning errors properly categorized

- **Hardened first-boot wizard**
  - `iso/airootfs/usr/local/bin/polymorph-first-boot`
  - Complete security rewrite
  - Input validation, logging, error handling

### Test Results
- Edge case tests: 14/14 passing
- Validation tests: 9/9 passing
- Total: 23/23 passing ✓

### Impact
This release prevents users from creating unbootable systems and protects against command injection attacks. All installations now enforce minimum viable system requirements (base + init + kernel).

**Upgrade Priority:** CRITICAL - All users should update immediately

### For More Information
- See `SECURITY.md` for complete audit report
- See `docs/SECURITY_AUDIT.md` for summary and testing procedures

### Phase 2 Improvements - 2026-01-23

#### Added
- **Quick Start Presets in Calamares**
  - New `scripts/generate_presets.py` - generates preset selector module
  - Preset descriptions with time/size estimates
  - Integration with build system
  
- **Installation Configuration Export**
  - New `scripts/export_config.py` - export installation configs
  - YAML format for machine-readable configs
  - Text format for human-readable summaries
  - Includes metadata (hostname, user, installation date)
  - Reproducible installation support

- **Enhanced Calamares Branding**
  - Updated `branding.desc` with comprehensive styling
  - Product information and URLs
  - Custom sidebar colors and styling
  - Window sizing and placement options
  - Support for product logos and images

- **First-Boot Wizard**
  - New `/usr/local/bin/polymorph-first-boot` wizard script
  - Automatic first-boot execution via autostart
  - Guided system update
  - Network configuration
  - Software installation assistance
  - User group configuration
  - Installation summary generation
  - Welcome messages and useful commands

- **Build System Enhancements**
  - Integrated preset generation into build.sh
  - Automatic executable permissions for first-boot wizard
  - Better organization and logging

- **Documentation Updates**
  - Enhanced README.md with Phase 2 features
  - Added preset information and quick start guides
  - Updated status and feature lists

#### Changed
- README.md now showcases all Phase 1 & 2 features
- Build script includes preset generation step
- Improved overall user experience documentation

### Phase 1 Improvements - 2026-01-23

#### Added
- **Compatibility Matrix System**
  - Created `config/compatibility-matrix.yaml` with comprehensive compatibility rules
  - Defined supported bases, desktops, init systems, and their interactions
  - Added known incompatibilities with severity levels (error/warning)
  - Included 6 pre-validated quick-start presets (minimal, desktop, gaming, developer, server, lightweight)
  - Documented filesystem requirements and time estimates

- **Configuration Validation**
  - New `scripts/validate_config.py` - comprehensive validation framework
  - Validates configurations against compatibility matrix
  - Checks base system, init system, desktop, filesystem, and kernel compatibility
  - Provides detailed error, warning, and info messages
  - Supports preset validation and custom config files
  - CLI interface with `--preset`, `--config`, and `--list-presets` options

- **Enhanced Build System**
  - Complete rewrite of `build.sh` with professional error handling
  - Colored output (info/success/warning/error)
  - Dependency checking (mkarchiso, python3, PyYAML)
  - Pre-build validation integration
  - Structured logging to `logs/build_TIMESTAMP.log`
  - Build time tracking and statistics
  - Automatic SHA256 checksum generation
  - Better error messages with actionable guidance

- **Testing Infrastructure**
  - Created `tests/` directory structure
  - Unit tests in `tests/test_validation.py`
    - Tests for valid/invalid configurations
    - Preset validation tests
    - Incompatibility detection tests
    - Filesystem validation tests
  - Integration tests in `tests/integration/test_build.sh`
    - Directory structure validation
    - Required files checking
    - Python syntax validation
    - Manifest generation testing
    - Configuration validation testing
  - Test documentation in `tests/README.md`

- **Documentation Structure**
  - New documentation hierarchy in `docs/`
  - `docs/README.md` - Documentation index
  - `docs/user/installation-guide.md` - Comprehensive installation guide
  - `docs/compatibility-matrix.md` - User-friendly compatibility reference
  - `docs/developer/contributing.md` - Contribution guidelines
  - `docs/developer/architecture.md` - Technical architecture overview
  - Enhanced existing `docs/build.md` documentation

#### Changed
- Build script now validates configurations before building
- Improved error handling throughout build process
- Better structured project with clear separation of concerns
- Enhanced logging and debugging capabilities

#### Fixed
- Build script now properly checks for all dependencies
- Improved error messages for common failure scenarios

## [0.1.0] - 2026-01-XX (Initial Version)

### Added
- Initial PolyMorph prototype
- Arch Linux base support
- Calamares installer integration
- KDE Plasma live environment
- Manifest-based package system
- Netinstall configuration generation
- Basic build system with mkarchiso
- Support for multiple kernels (linux, lts, zen, hardened)
- Desktop environment selection (KDE, GNOME, XFCE, etc.)
- Window manager options (i3, bspwm, dwm, openbox)
- Display server selection (Xorg, Wayland)
- Init system options (systemd, OpenRC, runit, s6)
- Filesystem tools (ext4, btrfs, xfs, f2fs, zfs)
- Network manager selection
- Audio server options (PipeWire, PulseAudio, ALSA)
- Graphics driver selection
- Virtualization support (KVM, VirtualBox, VMware)

### Project Structure
- `iso/` - archiso profile
- `calamares/` - Installer configuration
- `manifests/` - Package definitions
- `scripts/` - Build scripts
- `docs/` - Documentation

## [Future Releases]

### [2.0.0] - Multi-Distro Support (Planned)
- Debian base support
- Ubuntu base support
- Fedora base support
- openSUSE base support
- Gentoo base support
- Void Linux support
- Alpine Linux support
- Custom Calamares modules for multi-distro installation
- Base-specific post-install hooks
- Package name mapping across distributions

### [1.1.0] - UX Enhancements (Planned)
- Pre-installation compatibility checker in installer
- Installation summary export
- First-boot wizard
- Recovery mode in GRUB
- Enhanced Calamares branding
- Progress estimation during installation
- Real-time package count display

---

## Version History

- **0.1.0** - Initial prototype (Arch Linux only)
- **Phase 1** - Foundation improvements (validation, testing, docs)
- **1.1.0** - UX enhancements (planned)
- **2.0.0** - Multi-distro support (planned)

## Links

- [Repository](https://github.com/yourusername/polymorph)
- [Documentation](docs/README.md)
- [Issue Tracker](https://github.com/yourusername/polymorph/issues)
- [Releases](https://github.com/yourusername/polymorph/releases)
