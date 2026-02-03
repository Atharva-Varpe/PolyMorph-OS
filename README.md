# PolyMorph Linux

**One ISO. Any Distribution. Your Choice.**

A universal Linux installer that lets you install Arch, Debian, Ubuntu, Fedora, or any major distribution from a single ISO image. Boot once, choose your base distribution, customize everything, and install.

## Goal

Single Arch-based live ISO that can bootstrap and install ANY major Linux distribution with complete customization of kernels, init systems, desktops, drivers, and more - all validated for compatibility.

## Features

### Multi-Distribution Support
- **Base Distribution Selector** - Choose from Arch, Debian, Ubuntu, Fedora, openSUSE, Gentoo, Void, Alpine
- **Universal Bootstrap** - Automated base system installation for any selected distro
- **Live ISO Efficiency** - Single download works for all distributions

### Maximum Customization
- **Compatibility Matrix** - Validates all component combinations across distributions
- **Quick Start Presets** - Pre-configured installation profiles for common use cases
- **Full Control** - Choose kernels, init systems, desktops, drivers, filesystems
- **Configuration Export** - Save and share your custom configurations

### Professional Experience
- **Calamares Installer** - Modern, user-friendly installation interface
- **Enhanced Branding** - PolyMorph visual identity throughout
- **First-Boot Wizard** - Guided post-installation setup
- **Build Validation** - Pre-build and pre-install compatibility checks
- **Comprehensive Testing** - 23 automated tests ensuring quality

## Repo Layout

```
├── calamares/             # Installer configuration
│   ├── settings.conf      # Calamares sequence
│   ├── branding/          # PolyMorph theme
│   └── modules/           # Custom modules
│       ├── netinstall.yaml          # Package selections (auto-generated)
│       ├── polymorph_bootstrap.py   # Multi-distro installer module
│       └── preinstall_check.py      # Compatibility validation
├── config/
│   ├── compatibility-matrix.yaml    # Valid combinations
│   └── presets.yaml                 # Quick start profiles
├── manifests/             # Component packages (Arch-format for all distros)
│   ├── base.yaml          # Core system (distro-agnostic)
│   ├── desktops.yaml      # Desktop environments
│   ├── kernels.yaml       # Kernel options
│   └── ...
├── iso/                   # Archiso configuration
│   ├── packages.x86_64    # Live ISO packages (includes bootstrap tools)
│   └── airootfs/          # Live environment customization
├── scripts/
│   ├── generate_netinstall.py       # Build Calamares config from manifests
│   ├── validate_config.py           # Pre-build validation
│   └── export_config.py             # Save installation summaries
└── build.sh               # Main build script

## How It Works

1. **Boot Live ISO** - Arch-based live environment with all bootstrap tools
2. **Select Base Distribution** - Choose Arch, Debian, Ubuntu, Fedora, etc. in Calamares
3. **Customize Installation** - Pick kernel, init, desktop, drivers (validated for compatibility)
4. **Automated Bootstrap** - Custom module detects selection and calls appropriate installer:
   - Arch: `pacstrap` (native)
   - Debian/Ubuntu: `debootstrap`
   - Fedora: `dnf --installroot` (planned)
   - openSUSE: `zypper --root` (planned)
5. **Package Installation** - Selected components installed to target system
6. **First-Boot Setup** - Wizard runs on first login for final configuration

All from ONE universal ISO image.
├── iso/              # archiso profile
├── calamares/        # Installer config & branding  
├── manifests/        # Package definitions (data-driven)
├── config/           # Compatibility rules & presets
├── scripts/          # Build & validation tools
├── tests/            # Test suite
└── docs/             # Documentation
```

## 🚀 Build Quickstart

### Prerequisites
```bash
sudo pacman -S --needed archiso calamares python python-yaml
```

### Build ISO
```bash
./build.sh
```

### Test in QEMU
```bash
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom out/polymorph-*.iso
```

## 🎨 Quick Start Presets

Choose from pre-validated configurations:

| Preset | Description | Disk | Time |
|--------|-------------|------|------|
| **Minimal** | No GUI, command-line only | ~1.5GB | 10min |
| **Desktop** | KDE Plasma, modern setup | ~6GB | 30min |
| **Gaming** | Zen kernel, optimized | ~8GB | 45min |
| **Developer** | GNOME, dev tools, KVM | ~7GB | 40min |
| **Server** | Headless, LTS kernel | ~2GB | 15min |
| **Lightweight** | i3 WM, minimal resources | ~3GB | 20min |

Validate any preset:
```bash
python3 scripts/validate_config.py --preset desktop
```

## 🔧 Configuration

### Validate Configurations
```bash
# List available presets
python3 scripts/validate_config.py --list-presets

# Validate a preset
python3 scripts/validate_config.py --preset gaming

# Validate custom config
python3 scripts/validate_config.py --config my-config.yaml
```

### Export Installation Summary
```bash
python3 scripts/export_config.py
```

## 🧪 Testing

### Run Tests
```bash
# Unit tests (9/9 passing)
python3 tests/test_validation.py

# Integration tests
bash tests/integration/test_build.sh
```

## 📚 Documentation

- **[Build Guide](docs/build.md)** - Detailed build instructions
- **[Installation Guide](docs/user/installation-guide.md)** - How to install
- **[Compatibility Matrix](docs/compatibility-matrix.md)** - What works together
- **[Contributing](docs/developer/contributing.md)** - How to contribute
- **[Architecture](docs/developer/architecture.md)** - Technical details

## 🎁 Installation Features

### During Installation
- Choose from 6 quick-start presets or customize everything
- Real-time compatibility validation
- Clear error messages and warnings
- Time and size estimates

### Post-Installation
- **First-Boot Wizard** automatically runs to:
  - Update system packages
  - Configure network
  - Install additional software
  - Set up user groups
  - Generate installation summary

### Export Your Config
Save your installation configuration:
```bash
python3 scripts/export_config.py
```

Creates shareable YAML + human-readable summary for:
- Documentation
- Reproduction
- Troubleshooting
- Community sharing

## Calamares Features

- **Welcome** - Language selection
- **Locale** - Timezone & keyboard
- **Partition** - Manual or automatic
- **Users** - Account creation
- **Base Distribution** - Choose target OS (Arch/Debian/Ubuntu/Fedora/etc.)
- **Netinstall** - Component selection with preset support
- **Summary** - Review before install
- **Install** - Automated multi-distro bootstrap and package installation

## Distribution Support Status

| Distribution | Status | Bootstrap Tool | Notes |
|--------------|--------|----------------|-------|
| **Arch Linux** | ✅ Stable | pacstrap | Full support, 6 presets |
| **Debian** | 🧪 Experimental | debootstrap | Bookworm (12) supported |
| **Ubuntu** | 🧪 Experimental | debootstrap | Noble (24.04) supported |
| **Fedora** | 📋 Planned | dnf | Coming soon |
| **openSUSE** | 📋 Planned | zypper | Coming soon |
| **Gentoo** | 📋 Planned | stage3 | Coming soon |
| **Void Linux** | 📋 Planned | xbps | Coming soon |
| **Alpine** | 📋 Planned | apk | Coming soon |

## Testing Status

- **Validation Tests**: 9/9 passing
- **Integration Tests**: 14/14 passing  
- **Total Coverage**: 23/23 tests passing

## Version

**v1.0.0** - Universal Multi-Distribution Installer

Features:
- One ISO installs any distribution (Arch/Debian/Ubuntu + 5 more planned)
- Base distribution selector in Calamares
- Automated bootstrap for selected distro
- Compatibility validation across distributions
- Quick start presets for Arch
- Installation export and first-boot wizard
- Professional branding and UX
- Comprehensive testing and documentation

## Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/developer/contributing.md)

- Report bugs
- Suggest features
- Add package manifests
- Improve documentation
- Write tests

## 📜 License

See [LICENSE](LICENSE) file.

## 🔗 Links

- **Documentation**: [docs/README.md](docs/README.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Issues**: GitHub Issues
- **Community**: [Community Forums]

---

**Built with ♥ for maximum user choice and freedom**
