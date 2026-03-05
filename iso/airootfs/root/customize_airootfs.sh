#!/usr/bin/env bash
set -euo pipefail

# Minimal live environment tweaks. Extend as needed for networking, theming, etc.

# Set root password to 'root' for live session; change for release builds.
echo "root:root" | chpasswd

# Create live user
useradd -m -G wheel,audio,video,storage,optical,network -s /bin/bash polymorph
echo "polymorph:polymorph" | chpasswd
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/polymorph

# Set hostname for live session
echo "polymorph-live" > /etc/hostname

# Generate locale
echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

# Initialise pacman keyring (required for package installs in the installer)
pacman-key --init
pacman-key --populate archlinux

# Apply Calamares config overlay (overrides package defaults)
if [[ -d /root/calamares-overlay ]]; then
    mkdir -p /etc/calamares
    cp -af /root/calamares-overlay/. /etc/calamares/
    rm -rf /root/calamares-overlay
fi

# Enable basic services for live session
systemctl enable NetworkManager.service
systemctl enable sddm.service
