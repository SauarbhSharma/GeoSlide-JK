import os
import unittest
from pathlib import Path
from geoslide.audit.discovery import PathConfig

class TestPathConfigAndSafety(unittest.TestCase):
    def setUp(self):
        self.project_root = Path("D:/Projects/GeoSlide_JK").resolve()
        self.raw_root = Path("C:/Users/Saurabh Sharma/Downloads/J&K").resolve()

    def test_path_configuration(self):
        """Verify path config correctly resolves project and raw data roots."""
        cfg = PathConfig(raw_root=str(self.raw_root), project_root=str(self.project_root))
        self.assertEqual(cfg.project_root, self.project_root)
        self.assertEqual(cfg.raw_root, self.raw_root)
        self.assertEqual(cfg.output_root, self.project_root / "outputs")

    def test_prevention_of_raw_folder_writes(self):
        """Verify that attempting to configure output root inside raw data root raises PermissionError."""
        bad_output_inside_raw = str(self.raw_root / "output")
        with self.assertRaises(PermissionError):
            PathConfig(raw_root=str(self.raw_root), project_root=bad_output_inside_raw)

    def test_disjoint_roots(self):
        """Verify project root and raw root are disjoint."""
        cfg = PathConfig(raw_root=str(self.raw_root), project_root=str(self.project_root))
        self.assertFalse(cfg.project_root.is_relative_to(cfg.raw_root))
        self.assertFalse(cfg.raw_root.is_relative_to(cfg.project_root))

if __name__ == "__main__":
    unittest.main()
