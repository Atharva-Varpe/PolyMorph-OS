#!/bin/bash
set -euo pipefail

# ============================================================================
# PolyMorph ISO Build Script
# Enhanced with error handling, logging, and validation
# ============================================================================

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Error handler
error_exit() {
    log_error "$1"
    exit 1
}

# ============================================================================
# Initialization
# ============================================================================

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT" || error_exit "Failed to change to project directory"

BUILD_DATE=$(date +%Y%m%d_%H%M%S)
LOG_DIR="$PROJECT_ROOT/logs"
LOG_FILE="$LOG_DIR/build_${BUILD_DATE}.log"

# Create logs directory
mkdir -p "$LOG_DIR" || error_exit "Failed to create logs directory"

# Redirect output to log file as well
exec > >(tee -a "$LOG_FILE")
exec 2>&1

log_info "============================================================"
log_info "PolyMorph ISO Build Started: $(date)"
log_info "============================================================"

# ============================================================================
# Dependency Checks
# ============================================================================

log_info "Checking build dependencies..."

REQUIRED_COMMANDS=("mkarchiso" "python3" "sudo")
MISSING_DEPS=()

for cmd in "${REQUIRED_COMMANDS[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        MISSING_DEPS+=("$cmd")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    log_error "Missing required dependencies: ${MISSING_DEPS[*]}"
    log_error "Install with: sudo pacman -S --needed archiso python"
    exit 1
fi

log_success "All dependencies satisfied"

# ============================================================================
# Python Dependencies Check
# ============================================================================

log_info "Checking Python dependencies..."
if ! python3 -c "import yaml" 2>/dev/null; then
    log_warning "PyYAML not found, installing..."
    if ! python3 -m pip install --user pyyaml; then
        log_error "Failed to install PyYAML"
        log_error "Install manually with: python3 -m pip install --user pyyaml"
        exit 1
    fi
    log_success "PyYAML installed"
fi

# ============================================================================
# Pre-build Validation
# ============================================================================

log_info "Validating project structure..."

REQUIRED_DIRS=("iso" "calamares" "manifests" "scripts")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        error_exit "Required directory not found: $dir"
    fi
done

REQUIRED_FILES=("scripts/generate_netinstall.py" "iso/profiledef.sh")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        error_exit "Required file not found: $file"
    fi
done

log_success "Project structure validated"

# Make scripts executable
chmod +x scripts/*.py 2>/dev/null || true

# ============================================================================
# Configuration Validation (if validator exists)
# ============================================================================

if [ -f "scripts/validate_config.py" ] && [ -f "config/compatibility-matrix.yaml" ]; then
    log_info "Running configuration validation..."
    
    # Validate the default preset (desktop)
    if python3 scripts/validate_config.py --preset desktop --matrix config/compatibility-matrix.yaml; then
        log_success "Configuration validation passed"
    else
        log_warning "Configuration validation had warnings (continuing anyway)"
    fi
fi

# ============================================================================
# Generate Calamares Netinstall Manifest
# ============================================================================

log_info "Generating Calamares netinstall manifest..."

if ! python3 scripts/generate_netinstall.py; then
    error_exit "Failed to generate netinstall manifest"
fi

# Verify the output was created
if [ ! -f "calamares/modules/netinstall.yaml" ]; then
    error_exit "Netinstall manifest was not generated"
fi

log_success "Netinstall manifest generated"

# ============================================================================
# Generate Quick Start Presets
# ============================================================================

if [ -f "scripts/generate_presets.py" ]; then
    log_info "Generating quick start presets..."
    
    if python3 scripts/generate_presets.py; then
        log_success "Quick start presets generated"
    else
        log_warning "Failed to generate presets (continuing anyway)"
    fi
fi

# ============================================================================
# Sync Calamares Configuration
# ============================================================================

log_info "Syncing Calamares configuration into iso/airootfs..."

CALAMARES_DEST="iso/airootfs/etc/calamares"
rm -rf "$CALAMARES_DEST" || error_exit "Failed to remove old Calamares config"
mkdir -p "$CALAMARES_DEST" || error_exit "Failed to create Calamares directory"

if ! cp -a calamares/* "$CALAMARES_DEST"/; then
    error_exit "Failed to copy Calamares configuration"
fi

log_success "Calamares configuration synced"

# ============================================================================
# Set Executable Permissions
# ============================================================================

log_info "Setting executable permissions..."

# Make first-boot wizard executable
if [ -f "iso/airootfs/usr/local/bin/polymorph-first-boot" ]; then
    chmod +x "iso/airootfs/usr/local/bin/polymorph-first-boot"
    log_success "First-boot wizard permissions set"
fi

# ============================================================================
# Cleanup Previous Build Artifacts
# ============================================================================

log_info "Cleaning up previous work directories..."

if [ -d "work" ]; then
    log_info "Removing old work directory..."
    if ! sudo rm -rf work; then
        log_warning "Failed to remove work directory (continuing anyway)"
    fi
fi

if [ -d "out" ]; then
    log_info "Output directory 'out' exists (keeping old ISOs)"
fi

# ============================================================================
# Build ISO
# ============================================================================

log_info "============================================================"
log_info "Starting ISO build with mkarchiso..."
log_info "This may take several minutes..."
log_info "============================================================"

BUILD_START=$(date +%s)

if ! sudo mkarchiso -v -w work -o out iso; then
    error_exit "ISO build failed! Check the log at: $LOG_FILE"
fi

BUILD_END=$(date +%s)
BUILD_TIME=$((BUILD_END - BUILD_START))
BUILD_TIME_MIN=$((BUILD_TIME / 60))
BUILD_TIME_SEC=$((BUILD_TIME % 60))

log_success "ISO build completed in ${BUILD_TIME_MIN}m ${BUILD_TIME_SEC}s"

# ============================================================================
# Post-build Information
# ============================================================================

log_info "============================================================"
log_info "Build Summary"
log_info "============================================================"

# Find the generated ISO
ISO_FILE=$(find out -name "*.iso" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [ -n "$ISO_FILE" ]; then
    ISO_SIZE=$(du -h "$ISO_FILE" | cut -f1)
    ISO_NAME=$(basename "$ISO_FILE")
    
    log_success "ISO File: $ISO_NAME"
    log_success "ISO Size: $ISO_SIZE"
    log_success "Location: $ISO_FILE"
    
    # Generate checksum
    log_info "Generating SHA256 checksum..."
    (cd out && sha256sum "$ISO_NAME" > "${ISO_NAME}.sha256")
    log_success "Checksum saved: ${ISO_FILE}.sha256"
    
    # Test command
    log_info ""
    log_info "Test with QEMU:"
    echo "  qemu-system-x86_64 -enable-kvm -m 4096 -cdrom \"$ISO_FILE\""
else
    log_warning "ISO file not found in output directory"
fi

log_info ""
log_info "Build log saved to: $LOG_FILE"
log_info "============================================================"
log_success "Build complete!"
log_info "============================================================"
