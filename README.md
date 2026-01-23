# PolyMorph ISO Prototype

**Your Linux, Your Way** - Maximum choice, validated compatibility, easy installation.

## 🎯 Goal

Arch-based live ISO with Calamares installer that exposes maximum user choice (kernels, init systems, DE/WM, drivers, filesystems) while keeping the build reproducible and data-driven.

## ✨ Features

### Phase 1 ✅ (Foundation)
- ✅ **Compatibility Matrix** - Validates all component combinations
- ✅ **Configuration Validation** - Pre-build and pre-install checks
- ✅ **Professional Build System** - Error handling, logging, checksums
- ✅ **Comprehensive Testing** - Unit and integration tests
- ✅ **Extensive Documentation** - User guides and developer docs

### Phase 2 ✅ (UX Polish)
- ✅ **Quick Start Presets** - 6 pre-configured installation profiles
- ✅ **Installation Export** - Save and share configurations
- ✅ **Enhanced Branding** - Professional Calamares appearance
- ✅ **First-Boot Wizard** - Guided post-installation setup

### Future (Planned)
- 🔜 **Multi-Distro Support** - Debian, Ubuntu, Fedora, etc.
- 🔜 **Live Validation** - Pre-install compatibility checks in Calamares
- 🔜 **Community Features** - Configuration marketplace

## 📋 Repo Layout

```
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

## 🛠️ Calamares Features

- **Welcome** - Language selection
- **Locale** - Timezone & keyboard
- **Partition** - Manual or automatic
- **Users** - Account creation
- **Netinstall** - Package selection with presets
- **Summary** - Review before install

## 📊 Status


**Version 1.0** - Foundation & UX Polish Complete

- ✅ Phase 1: Validation, testing, documentation  
- ✅ Phase 2: Quick presets, export, first-boot wizard
- ⏳ Phase 3: Multi-distro support (planned)

**Current Build Target:**
- Base: Arch Linux
- Installer: Calamares with netinstall
- Live DE: KDE Plasma (Wayland)
- Validation: Comprehensive compatibility checks
- Testing: 9/9 tests passing

## 🤝 Contributing

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
