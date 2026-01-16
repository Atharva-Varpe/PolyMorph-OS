#!/bin/bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

echo "Building PolyMorph ISO (Version 1)..."

echo "Generating Calamares netinstall manifest..."
python3 scripts/generate_netinstall.py

echo "Syncing Calamares configuration into iso/airootfs..."
CALAMARES_DEST="iso/airootfs/etc/calamares"
rm -rf "$CALAMARES_DEST"
mkdir -p "$CALAMARES_DEST"
cp -a calamares/* "$CALAMARES_DEST"/

echo "Cleaning up previous work directories..."
if [ -d "work" ]; then
    sudo rm -rf work
fi
if [ -d "out" ]; then
    # Don't delete out, just let mkarchiso handle it or keep old ISOs
    echo "Output directory 'out' exists."
fi

echo "Starting build..."
sudo mkarchiso -v -w work -o out iso

echo "Build complete! ISO is in the 'out' directory."
