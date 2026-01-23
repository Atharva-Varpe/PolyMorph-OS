# PolyMorph Architecture

Technical overview of the PolyMorph Linux distribution build system.

## System Overview

PolyMorph is a data-driven Linux distribution installer that provides maximum user choice while maintaining compatibility and stability through automated validation.

### Key Components

```
┌─────────────────────────────────────────────────────┐
│              User Interface (Calamares)              │
├─────────────────────────────────────────────────────┤
│           Configuration Validation Layer             │
├──────────────┬──────────────────────┬───────────────┤
│   Manifest   │   Compatibility      │   Build       │
│   System     │   Matrix             │   System      │
└──────────────┴──────────────────────┴───────────────┘
       │                  │                    │
       ▼                  ▼                    ▼
   Package           Validation          ISO Creation
   Definitions        Rules              (mkarchiso)
```

## Architecture Layers

### 1. Manifest System

**Location:** `manifests/*.yaml`

**Purpose:** Data-driven package definitions organized by category.

**Structure:**
```yaml
category_name:
  option_name:
    packages: [pkg1, pkg2, pkg3]
    note: Description of this option
```

**Categories:**
- `base.yaml` - Base system targets
- `kernels.yaml` - Kernel variants
- `desktops.yaml` - Desktop environments
- `display.yaml` - Display servers
- `init.yaml` - Init systems
- `filesystems.yaml` - Filesystem tools
- `network.yaml` - Network managers
- `audio.yaml` - Audio servers
- `drivers.yaml` - Graphics drivers
- `virtualization.yaml` - VM solutions

**Advantages:**
- Single source of truth
- Easy to maintain
- Version controllable
- Community editable

### 2. Compatibility Matrix

**Location:** `config/compatibility-matrix.yaml`

**Purpose:** Define valid combinations and incompatibilities.

**Key Sections:**

**Bases:** Supported distributions with their capabilities
```yaml
bases:
  arch:
    status: "stable"
    package_managers: [pacman]
    init_systems: [systemd, openrc, runit, s6]
    kernels: [linux, linux-lts, linux-zen, linux-hardened]
```

**Incompatibilities:** Known problematic combinations
```yaml
incompatibilities:
  - name: "GNOME requires systemd"
    condition:
      desktop: gnome
      init: [openrc, runit, s6]
    reason: "GNOME has hard dependencies on systemd"
    severity: "error"
```

**Presets:** Pre-validated quick-start configurations
```yaml
presets:
  desktop:
    name: "Desktop Install"
    base: arch
    desktop: plasma-kde
    init: systemd
    ...
```

### 3. Validation System

**Location:** `scripts/validate_config.py`

**Purpose:** Validate configurations before installation.

**Flow:**
```
Configuration Input
    ├─→ Load Compatibility Matrix
    ├─→ Validate Base Selection
    ├─→ Check Init System Compatibility
    ├─→ Validate Desktop Requirements
    ├─→ Check Filesystem Requirements
    ├─→ Verify Kernel Compatibility
    ├─→ Check Incompatibilities
    └─→ Generate Validation Report
```

**Output:**
- ✅ Valid configurations
- ❌ Errors (blocking issues)
- ⚠️ Warnings (proceed with caution)
- 💡 Info (helpful tips)

**API:**
```python
validator = ConfigValidator(matrix_path)
result = validator.validate_config(config)
if result.is_valid:
    proceed_with_installation()
```

### 4. Netinstall Generator

**Location:** `scripts/generate_netinstall.py`

**Purpose:** Convert manifests to Calamares netinstall format.

**Process:**
```
Manifests (YAML)
    ↓
Parse & Load
    ↓
Generate Groups
    ├─→ Core System (immutable)
    ├─→ Bootloader (required)
    ├─→ Kernels (expandable)
    ├─→ Desktops (expandable)
    ├─→ Display Servers
    ├─→ ... (other categories)
    ↓
Write netinstall.yaml
    ↓
Copy to ISO
```

**Output:** `calamares/modules/netinstall.yaml`

### 5. Build System

**Location:** `build.sh`

**Purpose:** Orchestrate ISO creation with validation.

**Build Pipeline:**
```
┌──────────────────────┐
│ Check Dependencies   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Validate Structure   │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Run Config Validator │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Generate Netinstall  │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Sync Calamares       │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Build ISO (mkarchiso)│
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Generate Checksums   │
└──────────────────────┘
```

**Features:**
- Dependency checking
- Pre-build validation
- Error handling & logging
- Build time tracking
- Automatic checksum generation

### 6. Calamares Integration

**Location:** `calamares/`

**Components:**

**settings.conf** - Installation workflow
```
sequence:
  show: [welcome, locale, keyboard, partition, users, netinstall, summary]
  exec: [partition, mount, unpackfs, packages, bootloader, umount]
```

**modules/** - Module configurations
- `netinstall.yaml` - Package selection (generated)
- Custom modules (future: multi-distro support)

**branding/** - Visual customization
- `polymorph/branding.desc` - Name, colors, images

### 7. ISO Profile

**Location:** `iso/`

**archiso Structure:**

**profiledef.sh** - ISO metadata
```bash
iso_name="polymorph"
iso_version="0.1.0"
bootmodes=("bios.syslinux" "uefi.systemd-boot")
```

**packages.x86_64** - Live ISO packages
- Base system
- Desktop environment (KDE Plasma)
- Calamares installer
- Network tools
- Drivers

**airootfs/** - Live filesystem overlay
- `/etc/calamares/` - Installer config
- `/etc/skel/` - User skeleton files
- `/root/customize_airootfs.sh` - Live setup script

## Data Flow

### ISO Build Flow

```
manifests/*.yaml
    ↓
generate_netinstall.py
    ↓
calamares/modules/netinstall.yaml
    ↓
Sync to iso/airootfs/etc/calamares/
    ↓
mkarchiso builds ISO
    ↓
out/polymorph-*.iso
```

### Installation Flow

```
Boot ISO
    ↓
Live Environment (KDE Plasma)
    ↓
Launch Calamares
    ↓
User Selects Packages (netinstall)
    ↓
Validation (future: pre-install check)
    ↓
Partition Disk
    ↓
Install Packages (pacman)
    ↓
Configure System
    ↓
Install Bootloader
    ↓
Reboot to Installed System
```

## Design Principles

### 1. Data-Driven

All package definitions and compatibility rules are in declarative YAML files, not hardcoded in scripts.

**Benefits:**
- Easy to maintain
- Non-programmers can contribute
- Version controlled
- Automated validation

### 2. Validation-First

Validate configurations before building/installing to catch errors early.

**Validation Levels:**
- Build-time (ISO creation)
- Pre-install (future: in Calamares)
- Test-time (automated tests)

### 3. Modular & Extensible

Components are loosely coupled and can be extended independently.

**Extension Points:**
- Add manifests → automatic integration
- Add compatibility rules → automatic validation
- Add presets → instant availability
- Custom Calamares modules (future)

### 4. User Choice

Maximum flexibility while maintaining safety through validation.

**Philosophy:**
- Provide options
- Guide with presets
- Validate combinations
- Warn about issues
- Don't prevent (except errors)

## Future Architecture

### Multi-Distro Support (v2.0)

**Planned Changes:**

1. **Custom Calamares Module**
   ```python
   class PolyMorphInstaller:
       def detect_base(self, selection):
           # Route to appropriate bootstrapper
           
       def install_arch(self):
           # pacstrap + chroot
           
       def install_debian(self):
           # debootstrap
           
       def install_fedora(self):
           # dnf --installroot
   ```

2. **Base-Specific Hooks**
   ```
   hooks/
   ├── arch/
   │   ├── bootstrap.sh
   │   └── post-install.sh
   ├── debian/
   │   ├── bootstrap.sh
   │   └── post-install.sh
   └── ...
   ```

3. **Package Name Mapping**
   ```yaml
   packages:
     firefox:
       arch: firefox
       debian: firefox-esr
       fedora: firefox
   ```

## Performance Considerations

### Build Time

- **Caching:** Reuse work directory when possible
- **Parallel Downloads:** Multiple package downloads
- **Incremental Builds:** Only regenerate changed components

### ISO Size

- **Minimal Live Environment:** Only essential packages
- **Netinstall:** Download packages during installation
- **Compression:** zstd level 15 for squashfs

### Installation Time

- **Fast Mirrors:** Automatically select best mirror
- **Parallel Operations:** Where possible
- **Progress Indicators:** Keep user informed

## Security

### Build Security

- **Reproducible Builds:** Deterministic output
- **Checksum Verification:** SHA256 for all ISOs
- **Signed Packages:** Verify package signatures

### Installation Security

- **LUKS Encryption:** Full disk encryption option
- **Secure Boot:** Support (future)
- **Minimal Attack Surface:** Only install requested packages

## Debugging

### Build Logs

All builds logged to `logs/build_TIMESTAMP.log`

### Validation Output

```bash
python3 scripts/validate_config.py --preset desktop
# Shows errors, warnings, info
```

### Test Suite

```bash
# Unit tests
python3 tests/test_validation.py

# Integration tests
bash tests/integration/test_build.sh
```

## Development Workflow

```
1. Edit manifests or compatibility matrix
2. Validate changes
   └─→ python3 scripts/validate_config.py
3. Test manifest generation
   └─→ python3 scripts/generate_netinstall.py
4. Run tests
   └─→ python3 tests/test_validation.py
5. Build ISO
   └─→ ./build.sh
6. Test in QEMU
   └─→ qemu-system-x86_64 -m 4096 -cdrom out/*.iso
```

## References

- **archiso:** [Arch Linux ISO build system](https://wiki.archlinux.org/title/Archiso)
- **Calamares:** [Universal installer framework](https://calamares.io/)
- **Design Patterns:** Validation, Factory, Builder patterns

---

For implementation details, see source code documentation and inline comments.
