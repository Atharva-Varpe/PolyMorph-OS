#!/bin/bash
# Integration test for ISO build process
# Tests the build without actually creating the full ISO

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TEST_DIR="$PROJECT_ROOT/tests/integration"
TEMP_DIR="/tmp/polymorph_test_$$"

log_info() { echo -e "${GREEN}[TEST]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
log_success() { echo -e "${GREEN}[✓]${NC} $1"; }

cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup EXIT

test_manifest_generation() {
    log_info "Testing manifest generation..."
    
    mkdir -p "$TEMP_DIR"
    cd "$PROJECT_ROOT"
    
    if python3 scripts/generate_netinstall.py; then
        if [ -f "calamares/modules/netinstall.yaml" ]; then
            log_success "Manifest generation successful"
            return 0
        else
            log_error "Manifest file not created"
            return 1
        fi
    else
        log_error "Manifest generation failed"
        return 1
    fi
}

test_configuration_validation() {
    log_info "Testing configuration validation..."
    
    cd "$PROJECT_ROOT"
    
    # Test valid preset
    if python3 scripts/validate_config.py --preset desktop >/dev/null 2>&1; then
        log_success "Desktop preset validation passed"
    else
        log_error "Desktop preset validation failed"
        return 1
    fi
    
    # Test invalid config (create temp config)
    cat > "$TEMP_DIR/invalid.yaml" <<EOF
base: arch
init: openrc
desktop: gnome
EOF
    
    if ! python3 scripts/validate_config.py --config "$TEMP_DIR/invalid.yaml" >/dev/null 2>&1; then
        log_success "Invalid config correctly rejected"
    else
        log_error "Invalid config should have failed validation"
        return 1
    fi
    
    return 0
}

test_directory_structure() {
    log_info "Testing project directory structure..."
    
    cd "$PROJECT_ROOT"
    
    REQUIRED_DIRS=(
        "iso"
        "iso/airootfs"
        "calamares"
        "calamares/modules"
        "manifests"
        "scripts"
        "config"
        "docs"
        "tests"
    )
    
    for dir in "${REQUIRED_DIRS[@]}"; do
        if [ ! -d "$dir" ]; then
            log_error "Required directory missing: $dir"
            return 1
        fi
    done
    
    log_success "Directory structure validated"
    return 0
}

test_required_files() {
    log_info "Testing required files..."
    
    cd "$PROJECT_ROOT"
    
    REQUIRED_FILES=(
        "build.sh"
        "scripts/generate_netinstall.py"
        "scripts/validate_config.py"
        "config/compatibility-matrix.yaml"
        "iso/profiledef.sh"
        "calamares/settings.conf"
    )
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Required file missing: $file"
            return 1
        fi
    done
    
    log_success "Required files validated"
    return 0
}

test_script_syntax() {
    log_info "Testing Python script syntax..."
    
    cd "$PROJECT_ROOT"
    
    for script in scripts/*.py; do
        if ! python3 -m py_compile "$script" 2>/dev/null; then
            log_error "Syntax error in: $script"
            return 1
        fi
    done
    
    log_success "All Python scripts have valid syntax"
    return 0
}

# Run all tests
main() {
    echo "========================================"
    echo "PolyMorph Integration Tests"
    echo "========================================"
    echo
    
    TESTS=(
        "test_directory_structure"
        "test_required_files"
        "test_script_syntax"
        "test_manifest_generation"
        "test_configuration_validation"
    )
    
    PASSED=0
    FAILED=0
    
    for test in "${TESTS[@]}"; do
        if $test; then
            ((PASSED++))
        else
            ((FAILED++))
        fi
        echo
    done
    
    echo "========================================"
    echo "Test Results: $PASSED passed, $FAILED failed"
    echo "========================================"
    
    if [ $FAILED -eq 0 ]; then
        log_success "All integration tests passed!"
        return 0
    else
        log_error "Some tests failed"
        return 1
    fi
}

main
