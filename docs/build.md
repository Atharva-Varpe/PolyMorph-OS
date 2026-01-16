# PolyMorph build and install notes

## Version 1: Arch Linux Installer (Current Focus)

PolyMorph v1 is a **working Arch Linux installer** with user choice on kernels, DE/WM, audio, drivers, virtualization, and networking. It is **not yet a universal multi-distro installer**—that requires custom Calamares modules.

### Build prerequisites (on Arch)
- `sudo pacman -S --needed archiso calamares git base-devel`

### Build steps
1. From repo root: `./build.sh`
2. The script regenerates `calamares/modules/netinstall.yaml` from `manifests/`, syncs Calamares configs into `iso/airootfs/etc/calamares`, cleans `work/`, then runs `sudo mkarchiso -v -w work -o out iso`.
3. ISO outputs to `out/polymorph-*.iso`. Test via `qemu-system-x86_64 -enable-kvm -m 4096 -cdrom out/polymorph-*.iso`.

### Calamares workflow (v1)

**Live ISO includes:**
- Linux kernel, GRUB, EFI bootloader, firmware
- KDE Plasma (live environment)
- NetworkManager, essential drivers (Intel/AMD/NVIDIA GPU)
- Calamares installer

**Installation sequence:**
1. User boots ISO → KDE Plasma desktop
2. User runs Calamares (auto-launched or from menu)
3. Welcome, locale, keyboard settings
4. Partition disk (archiso partition module)
5. Choose username/password
6. **Netinstall step**: User selects from categories
7. Review selections → Install
8. Boot into new system

**What happens under the hood:**
- Calamares unpacks the live rootfs to target
- Runs `pacman` to install selected packages
- Generates fstab, locale, keyboard config
- Installs GRUB bootloader
- User reboots into Arch with their selections

### Calamares options mapping (v1)
- **Core System**: base, base-devel, firmware, ucode, sudo, nano (required, immutable)
- **Bootloader**: grub, efibootmgr, os-prober, dosfstools (required)
- **Kernels**: linux, lts, zen, hardened (with headers; user can pick multiple)
- **Desktop**: plasma-meta, plasma-wayland-session, sddm, dolphin
- **Window Managers**: i3, bspwm, dwm, openbox, xfce, lxde, lxqt, mate, cinnamon, gnome
- **Display**: xorg-server, xwayland, wayland
- **Init**: systemd, openrc, runit, s6
- **Filesystems**: e2fsprogs, btrfs-progs, xfsprogs, f2fs-tools, zfs-dkms, zfs-utils
- **Network**: networkmanager, wicd, connman, netctl
- **Audio**: pipewire, pulseaudio, alsa-utils
- **Graphics**: mesa, intel/amd/nouveau drivers, nvidia-dkms, open-vm-tools
- **Virtualization (optional)**: qemu-full, libvirt, virt-manager, virtualbox, open-vm-tools

---

## Version 2: Multi-Distro Support (Roadmap)

To support **Debian, Fedora, openSUSE, Gentoo, Void, Alpine** from a single ISO, we need custom Calamares Python modules that detect user base-target selection and route to appropriate bootstrap toolchain.

### Why This Isnt Done Yet

- Building multi-distro support requires: testing each bootstrap path (debootstrap, dnf --installroot, zypper, xbps, apk, Gentoo stage3), handling init systems differently per distro, managing package names, and custom Calamares module development + testing (1–2 weeks of work).

### Recommended Next Steps

1. **Ship Arch v1 now**: Perfect the Arch installer, test in QEMU/hardware.
2. **Gather feedback**: Does the UI flow work? Are packages available? Do systems boot?
3. **Plan Debian support**: Start with one additional base (Debian), then generalize.
4. **Custom module**: Once Debian works, refactor into a reusable multi-distro framework.

---

## Notes
- Live session autostarts Calamares via autostart entry in `airootfs/etc/skel/.config/autostart/calamares.desktop`.
- Root password in live session is set to `root` in `customize_airootfs.sh`; change for releases.
- Ensure internet connectivity during netinstall; packages are downloaded at install time.
- For ZFS on the installed system: After installation, run `zfs set canmount=noauto pool_name` and add zfs hooks to initramfs.
