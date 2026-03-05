# PolyMorph Linux

A single bootable ISO that installs any major Linux distribution. Boot once, pick your distro, and install — Arch, Debian, Ubuntu, Fedora, and more.

## Download

Get the latest release from the [releases page](https://github.com/Atharva-Varpe/PolyMorph-OS/releases).

## Distribution Support

| Distribution | Status         | Bootstrap     |
|--------------|----------------|---------------|
| Arch Linux   | Stable         | pacstrap      |
| Debian       | Experimental   | debootstrap   |
| Ubuntu       | Experimental   | debootstrap   |
| Fedora       | Planned        | dnf           |
| openSUSE     | Planned        | zypper        |
| Gentoo       | Planned        | stage3        |
| Void Linux   | Planned        | xbps          |
| Alpine       | Planned        | apk           |

## Build

Requires an Arch-based host with `archiso` installed.

```bash
sudo pacman -S --needed archiso python python-yaml
./build.sh
```

Output ISO is written to `out/`.

## Test

```bash
qemu-system-x86_64 -enable-kvm -m 4096 -cdrom out/polymorph-*.iso
```

## Repository Layout

```
iso/          archiso profile (live environment)
calamares/    installer config and branding
manifests/    package definitions
config/       compatibility rules and presets
scripts/      build and validation utilities
tests/        test suite
docs/         documentation
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
