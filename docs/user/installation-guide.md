# PolyMorph Installation Guide

Complete guide to installing PolyMorph Linux on your system.

## Prerequisites

### System Requirements

**Minimum:**
- CPU: 64-bit x86_64 processor
- RAM: 2 GB (4 GB recommended for desktop environments)
- Disk: 10 GB free space (20+ GB recommended)
- Internet connection (for netinstall packages)

**Recommended:**
- CPU: Multi-core 64-bit processor
- RAM: 4-8 GB
- Disk: 40+ GB SSD
- UEFI firmware (legacy BIOS supported)

### Download

Download the latest ISO from:
- **Official Site**: [polymorph.example.com/download](https://polymorph.example.com/download)
- **GitHub Releases**: [github.com/yourusername/polymorph/releases](https://github.com/yourusername/polymorph/releases)

**Verify the download:**
```bash
sha256sum -c polymorph-*.iso.sha256
```

### Create Bootable USB

**Linux:**
```bash
sudo dd if=polymorph-*.iso of=/dev/sdX bs=4M status=progress
sync
```

**Windows:**
- Use [Rufus](https://rufus.ie/) or [Etcher](https://www.balena.io/etcher/)
- Select ISO file and target USB drive
- Use DD mode for best compatibility

**macOS:**
```bash
diskutil list
sudo dd if=polymorph-*.iso of=/dev/diskX bs=4m
```

## Installation Process

### Step 1: Boot from USB

1. Insert USB drive
2. Restart computer
3. Enter boot menu (usually F12, F2, ESC, or DEL)
4. Select USB drive from boot menu
5. Wait for PolyMorph live environment to load

### Step 2: Live Environment

You'll boot into a KDE Plasma desktop environment. The Calamares installer will launch automatically.

**If installer doesn't auto-launch:**
- Click "Install PolyMorph" icon on desktop, or
- Open terminal and run: `sudo calamares`

### Step 3: Welcome Screen

- Select your language
- Review system requirements
- Click "Next"

### Step 4: Location & Keyboard

1. **Location**: Select your timezone
2. **Keyboard**: Choose keyboard layout
   - Test in the text box to verify
3. Click "Next"

### Step 5: Partitioning

Choose your partitioning strategy:

**Option A: Erase Disk (Recommended for beginners)**
- Wipes entire disk and uses automatic partitioning
- Creates ESP (512 MB), swap, and root partition
- ⚠️ **All data will be lost!**

**Option B: Replace Partition**
- Replaces existing partition with PolyMorph
- Keeps other partitions intact
- Good for dual-boot setups

**Option C: Manual Partitioning**
- Full control over partition layout
- Requires knowledge of Linux partitioning

**Recommended partition scheme (manual):**
```
/boot/efi  - 512 MB  - FAT32  - ESP flag
/          - 40+ GB  - ext4/btrfs
swap       - 4-8 GB  - swap
/home      - rest    - ext4/btrfs (optional)
```

**Encryption (optional):**
- Check "Encrypt system" for LUKS full-disk encryption
- Remember your passphrase!

Click "Next"

### Step 6: User Account

Create your user account:
- **Name**: Your full name
- **Username**: Login username (lowercase, no spaces)
- **Computer Name**: Hostname for your system
- **Password**: Strong password
- **Confirm Password**: Re-enter password

**Options:**
- ☑ Log in automatically (not recommended for security)
- ☑ Use same password for administrator (convenient but less secure)

Click "Next"

### Step 7: Package Selection (Netinstall)

This is where PolyMorph shines! Select components for your system:

#### Core System (Required)
- ☑ Base packages, firmware, utilities - **AUTO-SELECTED**

#### Bootloader (Required)
- ☑ GRUB bootloader - **AUTO-SELECTED**

#### Kernels (Select at least one)
- ☐ **Linux** - Latest stable kernel
- ☑ **Linux LTS** - Long-term support (recommended)
- ☐ **Linux Zen** - Optimized for desktop/gaming
- ☐ **Linux Hardened** - Security-focused

#### Desktop Environments (Select one)
- ☐ **KDE Plasma** - Modern, feature-rich (requires systemd)
- ☐ **GNOME** - Clean, user-friendly (requires systemd)
- ☐ **XFCE** - Lightweight, traditional
- ☐ **i3** - Tiling window manager (advanced)
- ☐ **MATE** - Traditional desktop
- ☐ **Cinnamon** - Modern traditional desktop
- ☐ **LXQt** - Ultra-lightweight Qt desktop

**Or use a window manager instead:**
- ☐ i3, bspwm, dwm, openbox (minimal, keyboard-driven)

#### Display Server
- ☑ **Xorg** - Traditional (recommended)
- ☐ **Wayland** - Modern (requires compatible DE)

#### Init System
- ☑ **systemd** - Modern (required for KDE/GNOME)
- ☐ **OpenRC** - Traditional
- ☐ **runit** - Minimal
- ☐ **s6** - Advanced

#### Filesystem Tools
- ☑ **ext4 tools** - Standard filesystem (recommended)
- ☐ **Btrfs tools** - Advanced features (snapshots, compression)
- ☐ **XFS tools** - High-performance
- ☐ **F2FS tools** - Flash-optimized
- ☐ **ZFS** - Advanced (requires compatible kernel)

#### Network Manager
- ☑ **NetworkManager** - Full-featured (recommended)
- ☐ **wicd** - Lightweight alternative
- ☐ **connman** - Intel connection manager
- ☐ **netctl** - Arch-native (command-line)

#### Audio Server
- ☑ **PipeWire** - Modern (recommended)
- ☐ **PulseAudio** - Traditional
- ☐ **ALSA only** - Minimal

#### Graphics Drivers
- ☑ **Open Source** - Mesa drivers (works for most GPUs)
- ☐ **NVIDIA Proprietary** - Better performance for NVIDIA
- ☐ **AMD Proprietary** - AMDGPU-PRO

#### Virtualization (Optional)
- ☐ **KVM/QEMU** - Full virtualization
- ☐ **VirtualBox** - Easy-to-use VM solution
- ☐ **VMware Tools** - For running as guest

**Quick Start Presets:**
- "Minimal" - No GUI, command-line only
- "Desktop" - KDE Plasma, modern setup
- "Gaming" - Optimized for gaming
- "Developer" - Development tools

**💡 Tip:** Hover over options for descriptions and compatibility info.

Click "Next"

### Step 8: Summary

Review all your selections:
- Partitions and formatting
- User account
- Selected packages
- Estimated installation time

Click "Install" to begin.

### Step 9: Installation

Installation progress will show:
- Partitioning and formatting
- Installing base system
- Downloading packages (internet required)
- Installing bootloader
- Configuring system

**Time estimate:**
- Minimal install: ~10 minutes
- Desktop install: ~30 minutes
- Full install with extras: ~45+ minutes

(Depends on internet speed and hardware)

☕ **Grab a coffee!**

### Step 10: Complete

When installation finishes:
1. Click "Restart now"
2. Remove USB drive when prompted
3. System will reboot into your new PolyMorph installation

## First Boot

### Login

1. Select your user from the list
2. Enter password
3. Press Enter

### Post-Installation Steps

1. **Update system:**
   ```bash
   sudo pacman -Syu
   ```

2. **Enable services (if needed):**
   ```bash
   sudo systemctl enable NetworkManager
   sudo systemctl start NetworkManager
   ```

3. **Install additional software:**
   ```bash
   sudo pacman -S firefox libreoffice
   ```

4. **Configure display drivers (NVIDIA):**
   ```bash
   sudo nvidia-xconfig  # If using proprietary drivers
   ```

## Troubleshooting

### Installation Issues

**"No internet connection"**
- Check ethernet cable
- Connect to WiFi from live environment first
- Try: `sudo systemctl restart NetworkManager`

**"Partitioning failed"**
- Ensure disk is not in use
- Try manual partitioning
- Check disk health: `sudo smartctl -a /dev/sdX`

**"Package download failed"**
- Check internet connection
- Verify mirror availability
- Try again (transient network issues)

**"Bootloader installation failed"**
- For UEFI: Ensure ESP partition is properly formatted (FAT32)
- For BIOS: Ensure boot flag is set on partition
- Check secure boot settings in BIOS

### Boot Issues

**"No bootable device found"**
- Enter BIOS and change boot order
- Disable secure boot (or configure MOK for signed kernels)
- Verify GRUB installation

**"Kernel panic"**
- Boot from USB, mount system, chroot
- Reinstall kernel: `pacman -S linux`
- Regenerate initramfs: `mkinitcpio -P`

**Black screen after boot**
- Try different kernel (append to GRUB: `nomodeset`)
- Check graphics drivers
- Try alternative display server (Xorg vs Wayland)

### Getting Help

- **Documentation**: [docs/troubleshooting.md](troubleshooting.md)
- **GitHub Issues**: Report bugs and get help
- **Community Forums**: Ask questions
- **IRC/Discord**: Real-time chat support

## Next Steps

- [Quick Start Guide](quick-start.md) - Configure your new system
- [FAQ](faq.md) - Common questions
- [Customize PolyMorph](customization.md) - Personalize your installation

---

**Welcome to PolyMorph! Enjoy your freedom of choice. 🎉**
