#!/usr/bin/env bash
set -euo pipefail

# Minimal live environment tweaks. Extend as needed for networking, theming, etc.

# Set root password to 'root' for live session; change for release builds.
echo "root:root" | chpasswd

# Enable basic services for live session
systemctl enable NetworkManager.service
systemctl enable sddm.service

# Autostart Calamares in the live user session (see autostart entry)

# Optional: preload keyrings to speed up installs
# pacman-key --init
# pacman-key --populate archlinux
