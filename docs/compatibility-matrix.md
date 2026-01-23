# PolyMorph Compatibility Matrix

This document describes which components work together and known incompatibilities.

## 🟢 Status Indicators

- **Stable** ✅ - Fully tested and supported
- **Experimental** ⚠️ - Works but not fully tested
- **Planned** 🔜 - Not yet implemented
- **Incompatible** ❌ - Does not work together

## Base Distributions

| Base | Status | Package Manager | Init Systems | Notes |
|------|--------|----------------|--------------|-------|
| Arch | ✅ Stable | pacman | systemd, openrc, runit, s6 | Full support |
| Debian | ⚠️ Experimental | apt | systemd, sysvinit | Bootstrap working |
| Ubuntu | ⚠️ Experimental | apt | systemd | Based on Debian |
| Fedora | ⚠️ Experimental | dnf | systemd | Requires testing |
| openSUSE | ⚠️ Experimental | zypper | systemd | Requires testing |
| Gentoo | ⚠️ Experimental | emerge | openrc, systemd | Compilation required |
| Void | ⚠️ Experimental | xbps | runit only | runit hardcoded |
| Alpine | ⚠️ Experimental | apk | openrc only | Musl-based |

## Desktop Environments

### Requirements Matrix

| Desktop | Init Required | Display Server | Min RAM | Status |
|---------|---------------|----------------|---------|--------|
| KDE Plasma | systemd | Wayland, Xorg | 2048 MB | ✅ |
| GNOME | systemd | Wayland, Xorg | 2048 MB | ✅ |
| XFCE | Any | Xorg | 768 MB | ✅ |
| MATE | Any | Xorg | 768 MB | ✅ |
| Cinnamon | systemd | Xorg | 2048 MB | ✅ |
| LXQt | Any | Xorg | 512 MB | ✅ |
| LXDE | Any | Xorg | 512 MB | ✅ |

### Window Managers

| WM | Init Required | Display Server | Min RAM | Status |
|----|---------------|----------------|---------|--------|
| i3 | Any | Xorg | 256 MB | ✅ |
| bspwm | Any | Xorg | 256 MB | ✅ |
| dwm | Any | Xorg | 128 MB | ✅ |
| Openbox | Any | Xorg | 256 MB | ✅ |

## Known Incompatibilities

### ❌ Critical Errors (Installation will fail)

| Combination | Reason | Alternative |
|-------------|--------|-------------|
| GNOME + OpenRC | GNOME requires systemd (logind) | Use systemd or different DE |
| KDE Plasma + OpenRC | Plasma requires systemd | Use systemd or different DE |
| Cinnamon + OpenRC | Cinnamon requires systemd | Use systemd or MATE/XFCE |
| i3/bspwm/dwm + Wayland | These WMs only support X11 | Use Xorg or Sway (i3-like for Wayland) |
| Void + systemd | Void is runit-only | Use runit or different base |
| Alpine + systemd | Alpine is OpenRC-only | Use OpenRC or different base |

### ⚠️ Warnings (May work with caveats)

| Combination | Issue | Workaround |
|-------------|-------|------------|
| ZFS + Zen kernel | DKMS may fail to build | Use LTS kernel or ext4/btrfs |
| ZFS + Hardened kernel | DKMS may fail to build | Use LTS kernel |
| Btrfs + Small disk | Overhead on small disks | Use ext4 for <20GB disks |
| Proprietary NVIDIA + Wayland | Inconsistent support | Use Xorg or wait for better driver support |

## Init System Compatibility

| Init | Desktop Support | Service Management | Complexity |
|------|----------------|-------------------|------------|
| systemd | All DEs | systemctl | Medium |
| OpenRC | XFCE, MATE, LXQt, WMs | rc-service | Medium |
| runit | XFCE, MATE, LXQt, WMs | sv | Low |
| s6 | XFCE, MATE, LXQt, WMs | s6-rc | High |

**Note:** GNOME, KDE Plasma, and Cinnamon require systemd.

## Filesystem Recommendations

| Filesystem | Use Case | Pros | Cons | Status |
|------------|----------|------|------|--------|
| ext4 | General purpose | Stable, fast | No advanced features | ✅ |
| Btrfs | Desktops, servers | Snapshots, compression | Complexity | ✅ |
| XFS | Large files, servers | High performance | No shrinking | ✅ |
| F2FS | SSDs, flash storage | Flash-optimized | Limited tools | ✅ |
| ZFS | Advanced users | Snapshots, checksums, RAID | Complex, kernel module | ⚠️ |

### Filesystem Requirements

- **ZFS**: Requires kernel headers, DKMS, 1+ GB RAM
- **Btrfs**: Requires btrfs-progs, 512+ MB RAM
- **XFS**: Requires xfsprogs, good for 16+ GB disks
- **F2FS**: Best for SSDs/eMMC storage

## Kernel Variants

| Kernel | Best For | Status |
|--------|----------|--------|
| linux | General use | ✅ |
| linux-lts | Stability, servers | ✅ |
| linux-zen | Gaming, desktop | ✅ |
| linux-hardened | Security-focused | ✅ |
| custom | Advanced users | 🔜 |

**Compatibility Notes:**
- ZFS works best with LTS kernel
- Gaming: Zen kernel recommended
- Servers: LTS kernel recommended

## Audio Servers

| Server | Status | Notes |
|--------|--------|-------|
| PipeWire | ✅ | Modern, recommended |
| PulseAudio | ✅ | Mature, widely compatible |
| ALSA only | ✅ | Minimal, no per-app volume |

## Network Managers

| Manager | Status | Best For |
|---------|--------|----------|
| NetworkManager | ✅ | Desktops, WiFi |
| netctl | ✅ | Servers, command-line |
| wicd | ✅ | Lightweight alternative |
| connman | ✅ | Embedded, minimal |

## Graphics Drivers

| Driver | GPU | Type | Status |
|--------|-----|------|--------|
| Mesa | Intel, AMD, NVIDIA | Open source | ✅ |
| NVIDIA | NVIDIA | Proprietary | ✅ |
| AMDGPU-PRO | AMD | Proprietary | ⚠️ |

**Recommendations:**
- **Intel**: Use mesa (open source)
- **AMD**: Use mesa (excellent performance)
- **NVIDIA**: Proprietary for better gaming performance

## Validation

All combinations are validated by the compatibility matrix system:

```bash
# Check a configuration
python3 scripts/validate_config.py --preset desktop

# Test custom configuration
python3 scripts/validate_config.py --config my-config.yaml
```

See [developer/testing.md](developer/testing.md) for more information.

## Quick Start Presets

Pre-validated configurations for common use cases:

| Preset | Base | Desktop | Init | Kernel | Filesystem |
|--------|------|---------|------|--------|------------|
| **Minimal** | Arch | None | systemd | LTS | ext4 |
| **Desktop** | Arch | KDE | systemd | linux | ext4 |
| **Gaming** | Arch | KDE | systemd | Zen | btrfs |
| **Developer** | Arch | GNOME | systemd | LTS | btrfs |
| **Server** | Arch | None | systemd | LTS | ext4 |
| **Lightweight** | Arch | i3 | runit | LTS | ext4 |

All presets are guaranteed to be compatible.

## Getting Help

If you encounter a compatibility issue not listed here:

1. Check the [FAQ](user/faq.md)
2. Run validation: `scripts/validate_config.py`
3. [Report an issue](https://github.com/yourusername/polymorph/issues)
4. Ask in community forums

## Contributing

Found a new incompatibility? Please:

1. Test and verify the issue
2. Document steps to reproduce
3. Submit a PR updating this document
4. Add test case in `tests/test_validation.py`

See [developer/contributing.md](developer/contributing.md) for details.
