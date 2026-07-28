import os
import tempfile
import unittest
from pathlib import Path
import yaml
from geoslide.audit.discovery import DataDiscoveryEngine, PathConfig

class TestDataDiscovery(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.tmp_dir.name)
        
        # Simulated raw root directory with sample structure
        self.sim_raw = (self.tmp_path / "sim_raw").resolve()
        self.sim_raw.mkdir()
        
        self.sim_project = (self.tmp_path / "sim_project").resolve()
        self.sim_project.mkdir()
        (self.sim_project / "outputs").mkdir()
        (self.sim_project / "configs").mkdir()

        # Create dummy source files for testing discovery
        (self.sim_raw / "single_file.tif").touch()
        
        (self.sim_raw / "multi_folder").mkdir()
        (self.sim_raw / "multi_folder" / "tile1.tif").touch()
        (self.sim_raw / "multi_folder" / "tile2.tif").touch()

        # Create mock config yaml
        self.mock_config_path = self.sim_project / "configs" / "data_paths.yaml"
        mock_data = {
            "test_category_single": "single_file.tif",
            "test_category_multi": "multi_folder/*.tif",
            "test_category_missing": "non_existent_file.tif"
        }
        with open(self.mock_config_path, "w") as f:
            yaml.dump(mock_data, f)

        self.path_cfg = PathConfig(raw_root=str(self.sim_raw), project_root=str(self.sim_project))
        self.engine = DataDiscoveryEngine(config_path=str(self.mock_config_path), path_config=self.path_cfg)

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_single_source_discovery(self):
        res = self.engine.discover_category("test_category_single", "single_file.tif")
        self.assertEqual(res["status"], "VERIFIED")
        self.assertEqual(res["match_count"], 1)

    def test_missing_file_reporting(self):
        res = self.engine.discover_category("test_category_missing", "non_existent_file.tif")
        self.assertEqual(res["status"], "MISSING")
        self.assertEqual(res["match_count"], 0)

    def test_ambiguous_or_multi_match_reporting(self):
        res = self.engine.discover_category("test_category_multi", "multi_folder/*.tif")
        self.assertEqual(res["status"], "MULTIPLE_MATCHES")
        self.assertEqual(res["match_count"], 2)

    def test_report_writing(self):
        report = self.engine.run_full_discovery()
        json_p, md_p = self.engine.write_reports(report)
        self.assertTrue(json_p.exists())
        self.assertTrue(md_p.exists())
        self.assertTrue(json_p.is_relative_to(self.sim_project / "outputs"))

if __name__ == "__main__":
    unittest.main()
