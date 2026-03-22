#!/usr/bin/env bash

iso_name="polymorph"
iso_label="POLYMORPH_$(date +%Y%m)"
iso_publisher="PolyMorph Project"
iso_application="PolyMorph Installer"
iso_version="1.2.0"
install_dir="arch"

bootmodes=(
  "bios.syslinux"
  "uefi.systemd-boot"
)

arch="x86_64"
pacman_conf="pacman.conf"

airootfs_image_type="squashfs"
airootfs_image_tool_options=("-comp" "zstd" "-Xcompression-level" "15")

file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root/customize_airootfs.sh"]="0:0:755"
  ["/usr/local/bin/polymorph-first-boot"]="0:0:755"
)
