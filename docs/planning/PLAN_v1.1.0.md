# PolyMorph Linux - v1.1.0 Plan (Fedora Support & Recovery)

## 🎯 Primary Feature: Fedora Base Support (Experimental)
**Goal:** Enable users to select "Fedora" as a base distribution in the installer.

### Implementation Steps
1.  **Bootstrap Module Update (`calamares/modules/polymorph_bootstrap.py`)**
    - Implement `bootstrap_fedora()` function.
    - Use `dnf --installroot` command.
    - Handle Fedora-specific GPG keys and repositories.
    - Ensure `dnf` is available in the live ISO (may need `pacman -S dnf` or custom build).

2.  **Manifest Creation (`manifests/fedora/`)**
    - Create `base.yaml` for Fedora minimal packages.
    - Map Arch package names to Fedora equivalents (e.g., `linux` -> `kernel`, `base-devel` -> `@development-tools`).

3.  **Compatibility Matrix Update (`config/compatibility-matrix.yaml`)**
    - Add `fedora` to supported bases.
    - Mark as `experimental`.
    - Define supported DEs/Kernels for Fedora base (start with GNOME/standard kernel).

## 🛠️ Secondary Feature: Recovery Mode in GRUB
**Goal:** Add a "Recovery Mode" entry to the installed system's GRUB menu.

### Implementation Steps
1.  **GRUB Config Modification**
    - Add a script to `calamares/modules/bootloader/` or a post-install hook.
    - Generate a `menuentry` with `single` or `emergency` kernel parameters.
    - Ensure root password is set or emergency shell is accessible.

## 🐛 Bug Fixes & Improvements
- **Review:** Check logs from recent `test_build.sh` runs.
- **Hardening:** Ensure `dnf` operations verify signatures.
- **UX:** Add "Experimental" badge to Fedora option in Calamares UI.

## 📅 Timeline
- **Week 1:** Fedora Bootstrap Logic + Manifests
- **Week 2:** Recovery Mode + Integration Tests
- **Week 3:** Validation & Release v1.1.0-alpha

## 📝 Notion Page Content
*Status: Ready to Create (Waiting for Credentials)*
