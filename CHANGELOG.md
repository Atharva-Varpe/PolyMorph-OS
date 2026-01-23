# PolyMorph Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
