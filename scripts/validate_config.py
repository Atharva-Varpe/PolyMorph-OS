#!/usr/bin/env python3
"""
Validate installation configurations against the compatibility matrix.
Can be used standalone or imported for pre-install validation.
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Any
from enum import Enum


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationResult:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.is_valid: bool = True
    
    def add_error(self, message: str):
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        self.warnings.append(message)
    
    def add_info(self, message: str):
        self.info.append(message)
    
    def print_report(self):
        """Print a formatted validation report."""
        if self.errors:
            print("\n❌ ERRORS:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.info:
            print("\n💡 INFO:")
            for info_msg in self.info:
                print(f"  • {info_msg}")
        
        if self.is_valid and not self.warnings:
            print("\n✅ Configuration is valid!")
        elif self.is_valid:
            print("\n✅ Configuration is valid (with warnings)")
        else:
            print("\n❌ Configuration validation failed!")
        
        return self.is_valid


class ConfigValidator:
    def __init__(self, matrix_path: Path):
        """Initialize validator with compatibility matrix."""
        with open(matrix_path, 'r') as f:
            self.matrix = yaml.safe_load(f)
    
    def validate_config(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate a configuration dictionary against the matrix."""
        result = ValidationResult()
        
        # Validate base system
        self._validate_base(config, result)
        
        # Validate component compatibility
        self._validate_init_system(config, result)
        self._validate_desktop(config, result)
        self._validate_filesystem(config, result)
        self._validate_kernel(config, result)
        
        # Check known incompatibilities
        self._check_incompatibilities(config, result)
        
        # Add helpful information
        self._add_estimates(config, result)
        
        return result
    
    def _validate_base(self, config: Dict, result: ValidationResult):
        """Validate base distribution selection."""
        base = config.get('base')
        
        # SECURITY: Validate base is provided and not empty
        if not base or not isinstance(base, str) or not base.strip():
            result.add_error("No base distribution specified - installation cannot proceed")
            result.is_valid = False
            return
        
        # SECURITY: Sanitize input to prevent injection
        base = base.strip().lower()
        
        if base not in self.matrix.get('bases', {}):
            result.add_error(f"Unknown base distribution: {base}")
            return
        
        base_info = self.matrix['bases'][base]
        status = base_info.get('status', 'unknown')
        
        if status == 'experimental':
            result.add_warning(f"Base distribution '{base}' is experimental and may not work correctly")
        elif status == 'deprecated':
            result.add_error(f"Base distribution '{base}' is deprecated and no longer supported")
        elif status == 'stable':
            result.add_info(f"Using stable base: {base}")
    
    def _validate_init_system(self, config: Dict, result: ValidationResult):
        """Validate init system compatibility with base."""
        base = config.get('base')
        init = config.get('init')
        
        # CRITICAL: Init system is required for installation
        if not base:
            return  # Base validation will catch this
        
        if not init or not isinstance(init, str) or not init.strip():
            result.add_error("Init system must be specified - system will not boot without it")
            result.is_valid = False
            return
        
        init = init.strip().lower()
        
        base_info = self.matrix.get('bases', {}).get(base, {})
        supported_inits = base_info.get('init_systems', [])
        
        if init not in supported_inits:
            result.add_error(
                f"Init system '{init}' is not supported on {base}. "
                f"Supported: {', '.join(supported_inits)}"
            )
    
    def _validate_desktop(self, config: Dict, result: ValidationResult):
        """Validate desktop environment requirements."""
        desktop = config.get('desktop')
        wm = config.get('wm')
        init = config.get('init')
        display_server = config.get('display_server')
        
        # Check desktop environment
        if desktop:
            desktop_info = self.matrix.get('desktops', {}).get(desktop, {})
            if not desktop_info:
                result.add_warning(f"Unknown desktop environment: {desktop}")
                return
            
            # Check init system requirements
            required_inits = desktop_info.get('requires_init', [])
            if init and init not in required_inits:
                result.add_error(
                    f"Desktop '{desktop}' requires init system: {', '.join(required_inits)}. "
                    f"Selected: {init}"
                )
            
            # Check display server
            supported_displays = desktop_info.get('display_servers', [])
            if display_server and display_server not in supported_displays:
                result.add_error(
                    f"Desktop '{desktop}' doesn't support display server '{display_server}'. "
                    f"Supported: {', '.join(supported_displays)}"
                )
            
            # Check RAM requirements
            min_ram = desktop_info.get('min_ram_mb', 0)
            if min_ram >= 2048:
                result.add_info(f"Desktop '{desktop}' requires at least {min_ram}MB RAM")
        
        # Check window manager
        if wm:
            wm_info = self.matrix.get('window_managers', {}).get(wm, {})
            if not wm_info:
                result.add_warning(f"Unknown window manager: {wm}")
                return
            
            required_inits = wm_info.get('requires_init', [])
            if init and init not in required_inits:
                result.add_warning(
                    f"Window manager '{wm}' works best with: {', '.join(required_inits)}"
                )
            
            supported_displays = wm_info.get('display_servers', [])
            if display_server and display_server not in supported_displays:
                result.add_error(
                    f"Window manager '{wm}' doesn't support '{display_server}'. "
                    f"Supported: {', '.join(supported_displays)}"
                )
    
    def _validate_filesystem(self, config: Dict, result: ValidationResult):
        """Validate filesystem requirements."""
        filesystem = config.get('filesystem')
        
        if not filesystem:
            return
        
        fs_reqs = self.matrix.get('filesystem_requirements', {}).get(filesystem, {})
        if fs_reqs:
            min_ram = fs_reqs.get('min_ram_mb', 0)
            if min_ram >= 1024:
                result.add_info(
                    f"Filesystem '{filesystem}' requires at least {min_ram}MB RAM"
                )
            
            notes = fs_reqs.get('notes')
            if notes:
                result.add_info(f"Filesystem '{filesystem}': {notes}")
    
    def _validate_kernel(self, config: Dict, result: ValidationResult):
        """Validate kernel compatibility."""
        base = config.get('base')
        kernel = config.get('kernel')
        
        # CRITICAL: Kernel is required for system to boot
        if not base:
            return  # Base validation will catch this
        
        if not kernel or not isinstance(kernel, str) or not kernel.strip():
            result.add_error("Kernel must be specified - system cannot boot without a kernel")
            result.is_valid = False
            return
        
        kernel = kernel.strip().lower()
        
        base_info = self.matrix.get('bases', {}).get(base, {})
        supported_kernels = base_info.get('kernels', [])
        
        if kernel not in supported_kernels:
            result.add_warning(
                f"Kernel '{kernel}' may not be available for {base}. "
                f"Supported: {', '.join(supported_kernels)}"
            )
    
    def _check_incompatibilities(self, config: Dict, result: ValidationResult):
        """Check against known incompatibilities."""
        incompats = self.matrix.get('incompatibilities', [])
        
        for incompat in incompats:
            condition = incompat.get('condition', {})
            matches = True
            
            # Check if all conditions match
            for key, values in condition.items():
                config_value = config.get(key)
                if not isinstance(values, list):
                    values = [values]
                
                if config_value not in values:
                    matches = False
                    break
            
            if matches:
                severity = incompat.get('severity', 'warning')
                message = f"{incompat.get('name', 'Incompatibility')}: {incompat.get('reason', 'No reason provided')}"
                
                if severity == 'error':
                    result.add_error(message)
                elif severity == 'warning':
                    result.add_warning(message)
                else:
                    result.add_info(message)
    
    def _add_estimates(self, config: Dict, result: ValidationResult):
        """Add installation time and size estimates."""
        desktop = config.get('desktop')
        wm = config.get('wm')
        base = config.get('base')
        
        estimates = self.matrix.get('time_estimates', {})
        
        if desktop or wm:
            time_est = estimates.get('base_with_desktop', 30)
        else:
            time_est = estimates.get('base_minimal', 10)
        
        if base == 'gentoo':
            factor = estimates.get('gentoo_compile_factor', 6.0)
            time_est = int(time_est * factor)
            result.add_info(f"Estimated installation time: ~{time_est} minutes (compilation required)")
        else:
            result.add_info(f"Estimated installation time: ~{time_est} minutes")
    
    def get_preset(self, preset_name: str) -> Dict[str, Any]:
        """Get a preset configuration by name."""
        presets = self.matrix.get('presets', {})
        return presets.get(preset_name, {})
    
    def list_presets(self) -> List[Tuple[str, str]]:
        """List all available presets with descriptions."""
        presets = self.matrix.get('presets', {})
        return [(name, info.get('description', '')) for name, info in presets.items()]


def main():
    """Command-line interface for validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate PolyMorph installation configuration')
    parser.add_argument('--config', type=str, help='Path to configuration YAML file')
    parser.add_argument('--preset', type=str, help='Validate a preset configuration')
    parser.add_argument('--list-presets', action='store_true', help='List available presets')
    parser.add_argument(
        '--matrix',
        type=str,
        default='config/compatibility-matrix.yaml',
        help='Path to compatibility matrix (default: config/compatibility-matrix.yaml)'
    )
    
    args = parser.parse_args()
    
    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    matrix_path = project_root / args.matrix
    
    if not matrix_path.exists():
        print(f"❌ Compatibility matrix not found: {matrix_path}", file=sys.stderr)
        return 1
    
    validator = ConfigValidator(matrix_path)
    
    # List presets
    if args.list_presets:
        print("\n📋 Available Presets:\n")
        for name, desc in validator.list_presets():
            print(f"  • {name:15} - {desc}")
        return 0
    
    # Load configuration
    config = None
    config_name = "custom"
    
    if args.preset:
        config = validator.get_preset(args.preset)
        config_name = args.preset
        if not config:
            print(f"❌ Preset '{args.preset}' not found", file=sys.stderr)
            return 1
    elif args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"❌ Config file not found: {config_path}", file=sys.stderr)
            return 1
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        print("❌ Either --config or --preset must be specified", file=sys.stderr)
        parser.print_help()
        return 1
    
    # Validate
    print(f"\n🔍 Validating configuration: {config_name}\n")
    result = validator.validate_config(config)
    result.print_report()
    
    return 0 if result.is_valid else 1


if __name__ == '__main__':
    sys.exit(main())
