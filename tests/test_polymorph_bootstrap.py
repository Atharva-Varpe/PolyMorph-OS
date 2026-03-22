#!/usr/bin/env python3

import importlib.util
import sys
import unittest
from pathlib import Path


def load_polymorph_bootstrap_module():
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / "calamares" / "modules" / "polymorph_bootstrap.py"
    spec = importlib.util.spec_from_file_location("polymorph_bootstrap", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Failed to create module spec")
    module = importlib.util.module_from_spec(spec)
    # Register in sys.modules before exec so @dataclass can resolve the module
    sys.modules["polymorph_bootstrap"] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop("polymorph_bootstrap", None)
        raise
    return module


class TestPolymorphBootstrapSelection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pb = load_polymorph_bootstrap_module()

    def test_extract_packages_from_package_operations(self):
        ops = [
            {
                "source": "netinstall",
                "install": ["grub", {"package": "os-prober", "pre-script": "x", "post-script": "y"}],
            },
            {"source": "netinstall", "try_install": ["__POLYMORPH_BASE__ARCH__"]},
        ]
        pkgs = self.pb._extract_packages_from_package_operations(ops)
        self.assertIn("grub", pkgs)
        self.assertIn("os-prober", pkgs)
        self.assertIn("__POLYMORPH_BASE__ARCH__", pkgs)

    def test_detect_base_from_marker(self):
        base = self.pb._detect_base_from_markers(["foo", "__POLYMORPH_BASE__DEBIAN__", "bar"])
        self.assertEqual(base, "debian")

    def test_detect_multiple_markers_raises(self):
        with self.assertRaises(ValueError):
            self.pb._detect_base_from_markers([
                "__POLYMORPH_BASE__ARCH__",
                "__POLYMORPH_BASE__DEBIAN__",
            ])

    def test_filter_out_markers(self):
        pkgs = self.pb._filter_out_markers([
            "__POLYMORPH_BASE__ARCH__",
            "grub",
            "__POLYMORPH_BASE__DEBIAN__",
            "linux",
        ])
        self.assertEqual(pkgs, ["grub", "linux"])

    def test_detect_fedora_marker(self):
        base = self.pb._detect_base_from_markers(["kernel", "__POLYMORPH_BASE__FEDORA__", "grub2"])
        self.assertEqual(base, "fedora")

    def test_fedora_in_supported_bases(self):
        self.assertIn("fedora", self.pb.SUPPORTED_BASES)

    def test_validate_package_names_rejects_empty(self):
        result = self.pb._validate_package_names(["", "  ", "grub", None])
        self.assertEqual(result, ["grub"])

    def test_validate_package_names_rejects_injection(self):
        result = self.pb._validate_package_names(["vim; rm -rf /", "grub", "linux"])
        self.assertEqual(result, ["grub", "linux"])


if __name__ == "__main__":
    unittest.main()
