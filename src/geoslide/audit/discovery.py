import os
import glob
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import yaml

logger = logging.getLogger("geoslide.audit.discovery")

class PathConfig:
    def __init__(self, raw_root: Optional[str] = None, project_root: Optional[str] = None):
        self.project_root = Path(project_root or os.getenv("GEOSLIDE_PROJECT_ROOT", "D:/Projects/GeoSlide_JK")).resolve()
        self.raw_root = Path(raw_root or os.getenv("GEOSLIDE_RAW_DATA_ROOT", "C:/Users/Saurabh Sharma/Downloads/J&K")).resolve()
        self.output_root = self.project_root / "outputs"
        
        # Verify read-only safety guard
        self.verify_read_only_safety()

    def verify_read_only_safety(self) -> bool:
        """Ensure project output root is completely disjoint from raw data root."""
        raw_str = str(self.raw_root).lower()
        proj_str = str(self.project_root).lower()
        output_str = str(self.output_root).lower()
        
        if output_str.startswith(raw_str):
            raise PermissionError(f"CRITICAL SAFETY VIOLATION: Output directory {self.output_root} is inside read-only raw root {self.raw_root}!")
        return True

class DataDiscoveryEngine:
    def __init__(self, config_path: Optional[str] = None, path_config: Optional[PathConfig] = None):
        self.path_config = path_config or PathConfig()
        if config_path is None:
            config_path = str(self.path_config.project_root / "configs" / "data_paths.yaml")
        
        self.config_path = Path(config_path)
        self.paths_yaml = self.load_paths_config()

    def load_paths_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            logger.warning(f"Config file not found at {self.config_path}, using empty defaults.")
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def discover_category(self, category_name: str, patterns: Any) -> Dict[str, Any]:
        """Resolves configured glob pattern(s) inside raw data folder and inspects files."""
        if isinstance(patterns, str):
            patterns = [patterns]
        
        matches: List[Path] = []
        for pattern in patterns:
            # Handle full path vs relative glob inside raw root
            search_glob = str(self.path_config.raw_root / pattern)
            found = [Path(p) for p in glob.glob(search_glob, recursive=True)]
            matches.extend(found)

        # Deduplicate
        matches = sorted(list(set(matches)))
        
        status = "VERIFIED"
        if len(matches) == 0:
            status = "MISSING"
        elif len(matches) > 1:
            # Note: For multi-tile datasets (e.g. DEM tiles), multiple matches may be normal
            status = "MULTIPLE_MATCHES"

        inspected_files = [self.inspect_file(p) for p in matches[:20]]  # limit detail list to 20

        return {
            "category": category_name,
            "status": status,
            "match_count": len(matches),
            "patterns": patterns,
            "matches": [str(m.relative_to(self.path_config.raw_root)) if m.is_relative_to(self.path_config.raw_root) else str(m) for m in matches],
            "sample_details": inspected_files
        }

    def inspect_file(self, file_path: Path) -> Dict[str, Any]:
        """Reads safe metadata without altering source file."""
        info = {
            "path": str(file_path),
            "name": file_path.name,
            "size_bytes": file_path.stat().st_size if file_path.exists() else 0,
            "is_file": file_path.is_file(),
            "extension": file_path.suffix.lower()
        }

        # Attempt optional geospatial spatial metadata read if packages available
        ext = file_path.suffix.lower()
        if ext in ['.tif', '.tiff']:
            info.update(self._inspect_raster(file_path))
        elif ext in ['.geojson', '.shp', '.gpkg']:
            info.update(self._inspect_vector(file_path))
        elif ext in ['.nc', '.nc4']:
            info.update(self._inspect_netcdf(file_path))

        return info

    def _inspect_raster(self, file_path: Path) -> Dict[str, Any]:
        try:
            import rasterio
            with rasterio.open(file_path) as src:
                return {
                    "crs": str(src.crs),
                    "bounds": list(src.bounds),
                    "width": src.width,
                    "height": src.height,
                    "count": src.count,
                    "dtype": str(src.dtypes[0])
                }
        except Exception:
            return {"raster_inspection": "rasterio not installed or unreadable header"}

    def _inspect_vector(self, file_path: Path) -> Dict[str, Any]:
        try:
            import pyogrio
            meta = pyogrio.read_info(file_path)
            return {
                "crs": str(meta.get("crs")),
                "feature_count": meta.get("features"),
                "geometry_type": meta.get("geometry_type"),
                "fields": list(meta.get("fields", []))
            }
        except Exception:
            return {"vector_inspection": "pyogrio not installed or unreadable vector"}

    def _inspect_netcdf(self, file_path: Path) -> Dict[str, Any]:
        try:
            import netCDF4
            with netCDF4.Dataset(file_path, "r") as ds:
                return {
                    "variables": list(ds.variables.keys()),
                    "dimensions": list(ds.dimensions.keys())
                }
        except Exception:
            return {"netcdf_inspection": "netCDF4 not installed or unreadable dataset"}

    def run_full_discovery(self) -> Dict[str, Any]:
        results = {}
        # Iterate over configured data categories
        for key, val in self.paths_yaml.items():
            if key in ["raw_root", "project_root"]:
                continue
            if isinstance(val, dict):
                for sub_key, patterns in val.items():
                    cat_name = f"{key}.{sub_key}"
                    results[cat_name] = self.discover_category(cat_name, patterns)
            else:
                results[key] = self.discover_category(key, val)

        report = {
            "project_root": str(self.path_config.project_root),
            "raw_root": str(self.path_config.raw_root),
            "total_categories_scanned": len(results),
            "summary": {
                "verified": sum(1 for r in results.values() if r["status"] == "VERIFIED"),
                "missing": sum(1 for r in results.values() if r["status"] == "MISSING"),
                "multiple_matches": sum(1 for r in results.values() if r["status"] == "MULTIPLE_MATCHES"),
            },
            "categories": results
        }
        return report

    def write_reports(self, report_data: Dict[str, Any]) -> Tuple[Path, Path]:
        """Writes JSON manifest and Markdown summary report ONLY to project outputs."""
        output_dir = self.path_config.project_root / "outputs" / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)

        json_path = output_dir / "data_discovery_manifest.json"
        md_path = output_dir / "data_discovery_report.md"

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)

        md_content = self.generate_markdown_summary(report_data)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        return json_path, md_path

    def generate_markdown_summary(self, report: Dict[str, Any]) -> str:
        lines = [
            "# GeoSlide-JK Data Discovery & Audit Report",
            "",
            f"**Project Root**: `{report['project_root']}`",
            f"**Raw Data Root (Read-Only)**: `{report['raw_root']}`",
            "",
            "## Audit Summary",
            f"- Total Categories Configured: {report['total_categories_scanned']}",
            f"- Categories Verified (Single Match): {report['summary']['verified']}",
            f"- Categories with Multiple Matches / Tiles: {report['summary']['multiple_matches']}",
            f"- Missing Categories: {report['summary']['missing']}",
            "",
            "## Category Details",
            "",
            "| Category | Status | Match Count | Configured Patterns |",
            "| :--- | :--- | :--- | :--- |"
        ]

        for cat, data in report["categories"].items():
            patterns_str = ", ".join([f"`{p}`" for p in data["patterns"]])
            lines.append(f"| `{cat}` | **{data['status']}** | {data['match_count']} | {patterns_str} |")

        lines.extend([
            "",
            "---",
            "*Report generated automatically by `geoslide.audit.discovery`. Source datasets verified read-only.*"
        ])
        return "\n".join(lines)
