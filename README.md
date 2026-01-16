# PolyMorph ISO Prototype

Goal: Arch-based live ISO with Calamares installer that exposes maximum user choice (kernels, init systems, DE/WM, drivers, filesystems) while keeping the build reproducible and data-driven.

Repo layout
- `iso/` — archiso profile (packages, pacman.conf, profiledef.sh, airootfs hooks)
- `calamares/` — Calamares settings/modules, branding placeholders
- `manifests/` — data-driven package sets for selectable components
- `scripts/` — helper scripts to generate Calamares netinstall entries and post-install hooks
- `docs/` — build/run notes

Status
- Starting from scratch. Arch base + Calamares + Plasma (Wayland) as initial target; extend via manifests.

Build quickstart
- Install deps: `sudo pacman -S --needed archiso calamares`
- Build: `cd iso && sudo mkarchiso -v .`
- Test: `qemu-system-x86_64 -enable-kvm -m 4096 -cdrom out/polymorph-*.iso`

Calamares
- Config lives in `calamares/` and is copied into `iso/airootfs/etc/calamares/` for the live ISO.
- Netinstall options cover bases, kernels, DE/WM, init, filesystems, package managers, network, audio, drivers, virtualization. See `docs/build.md` for mapping and requirements.
