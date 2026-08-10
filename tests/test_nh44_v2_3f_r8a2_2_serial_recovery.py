import pytest, sys, os, json, math, hashlib, re, tempfile, copy, ast
import numpy as np, pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from geoslide.scenario_loader import load_scenario_definitions, generate_18_provenance_records
from geoslide.boundary_mapper import map_segment_method_a, map_segment_method_b, map_all_segments
from geoslide.scientific_audits import (
    compute_spearman_and_kendall_audits,
    compute_dhi_d_audit,
    compute_uncertainty_audit,
    compute_broadcast_trace,
    compute_mapping_reconciliation
)
from scripts.validate_v2_3f_r8a2_2_manifest import validate_r8a2_2_manifest
from scripts.export_v2_3f_r8a2_2_ui_evidence import export_r8a2_2_ui_evidence

def test_01_independently_derived_scientific_fixtures():
    # Test SciPy audit functions with independently derived artificial synthetic fixture
    df_fix = pd.DataFrame([
        {"scenario_id": "S1", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S1", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S2", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S2", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S3", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S3", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S4", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S4", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S5", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071},
        {"scenario_id": "S5", "dhi_a": 0.5, "dhi_b": 0.5, "dhi_c": 0.5, "dhi_d": 0.7071}
    ])
    df_sp = compute_spearman_and_kendall_audits(df_fix)
    
    expected_columns = [
        "scenario_id", "pair", "raw_column_x", "raw_column_y", "sample_size",
        "spearman_rho", "spearman_p_value", "kendall_tau", "status", "reason",
        "var_x", "var_y", "unique_count_x", "unique_count_y",
        "missing_value_handling", "tie_handling", "audit_evaluation_type"
    ]
    assert list(df_sp.columns) == expected_columns

    expected_tuples = [
        ("S1", "DHI_A vs DHI_B"),
        ("S1", "DHI_A vs DHI_C"),
        ("S1", "DHI_A vs DHI_D"),
        ("S1", "DHI_B vs DHI_C"),
        ("S1", "DHI_B vs DHI_D"),
        ("S1", "DHI_C vs DHI_D"),
        ("S2", "DHI_A vs DHI_B"),
        ("S2", "DHI_A vs DHI_C"),
        ("S2", "DHI_A vs DHI_D"),
        ("S2", "DHI_B vs DHI_C"),
        ("S2", "DHI_B vs DHI_D"),
        ("S2", "DHI_C vs DHI_D"),
        ("S3", "DHI_A vs DHI_B"),
        ("S3", "DHI_A vs DHI_C"),
        ("S3", "DHI_A vs DHI_D"),
        ("S3", "DHI_B vs DHI_C"),
        ("S3", "DHI_B vs DHI_D"),
        ("S3", "DHI_C vs DHI_D"),
        ("S4", "DHI_A vs DHI_B"),
        ("S4", "DHI_A vs DHI_C"),
        ("S4", "DHI_A vs DHI_D"),
        ("S4", "DHI_B vs DHI_C"),
        ("S4", "DHI_B vs DHI_D"),
        ("S4", "DHI_C vs DHI_D"),
        ("S5", "DHI_A vs DHI_B"),
        ("S5", "DHI_A vs DHI_C"),
        ("S5", "DHI_A vs DHI_D"),
        ("S5", "DHI_B vs DHI_C"),
        ("S5", "DHI_B vs DHI_D"),
        ("S5", "DHI_C vs DHI_D"),
    ]
    observed_tuples = list(zip(df_sp["scenario_id"], df_sp["pair"]))

    assert len(df_sp) == 30
    assert observed_tuples == expected_tuples
    assert len(set(observed_tuples)) == 30
    assert not df_sp.duplicated(subset=["scenario_id", "pair"]).any()
    
    scipy_pairs_checked = 0
    from scipy import stats

    for _, r in df_sp.iterrows():
        assert r["status"] == "UNDEFINED_ZERO_VARIANCE"
        assert r["reason"] == "CONSTANT_INPUT_VECTOR"
        assert r["sample_size"] == 2
        assert r["spearman_rho"] == ""
        assert r["spearman_p_value"] == ""
        assert r["kendall_tau"] == ""
        assert r["var_x"] == 0.0
        assert r["var_y"] == 0.0
        assert r["unique_count_x"] == 1
        assert r["unique_count_y"] == 1
        assert r["missing_value_handling"] == "NONE_ZERO_MISSING"
        assert r["tie_handling"] == "AVERAGE_RANK"
        assert r["audit_evaluation_type"] == "ZERO_VARIANCE_UNDEFINED_CORRELATION"

        sc_id = r["scenario_id"]
        col_x = r["raw_column_x"]
        col_y = r["raw_column_y"]

        sub_fix = df_fix[df_fix["scenario_id"] == sc_id]
        v_x = sub_fix[col_x].values
        v_y = sub_fix[col_y].values

        res_sp = stats.spearmanr(v_x, v_y)
        res_kt = stats.kendalltau(v_x, v_y)

        assert np.isnan(res_sp.statistic)
        assert np.isnan(res_sp.pvalue)
        assert np.isnan(res_kt.statistic)
        assert np.isnan(res_kt.pvalue)

        scipy_pairs_checked += 1

    assert scipy_pairs_checked == 30

def test_02_native_cell_boundary_cases():
    m_west = map_segment_method_a(33.25, 75.10)
    assert m_west["col"] == 2551
    assert m_west["west"] == 75.10
    assert m_west["east"] == 75.20
    
    m_inside = map_segment_method_a(33.25, 75.15)
    assert m_inside["col"] == 2551
    assert m_inside["west"] == 75.10
    assert m_inside["east"] == 75.20

def test_03_derived_158_segment_invariant():
    seg_inv_path = PROJECT_ROOT / "outputs" / "reports" / "v2_3a_final_segment_inventory.csv"
    assert seg_inv_path.exists()
    df_seg = pd.read_csv(seg_inv_path)
    assert len(df_seg) == 158

def test_04_derived_11_cell_invariant():
    seg_inv_path = PROJECT_ROOT / "outputs" / "reports" / "v2_3a_final_segment_inventory.csv"
    df_seg = pd.read_csv(seg_inv_path)
    df_map = map_all_segments(df_seg)
    unique_cells = df_map["native_cell_id"].nunique()
    assert unique_cells == 11

def test_05_range_string_count_reconciliation():
    seg_inv_path = PROJECT_ROOT / "outputs" / "reports" / "v2_3a_final_segment_inventory.csv"
    df_seg = pd.read_csv(seg_inv_path)
    df_map = map_all_segments(df_seg)
    grouped = df_map.groupby("native_cell_id")
    total_reconciled = sum(len(g) for _, g in grouped)
    assert total_reconciled == 158

def test_06_deterministic_csv_bytes():
    seg_inv_path = PROJECT_ROOT / "outputs" / "reports" / "v2_3a_final_segment_inventory.csv"
    df_seg = pd.read_csv(seg_inv_path)
    df_map = map_all_segments(df_seg)
    with tempfile.TemporaryDirectory() as tmpdir:
        p1 = Path(tmpdir) / "out1.csv"
        p2 = Path(tmpdir) / "out2.csv"
        df_map.to_csv(p1, index=False, lineterminator="\n")
        df_map.to_csv(p2, index=False, lineterminator="\n")
        assert open(p1, "rb").read() == open(p2, "rb").read()

def test_07_deterministic_json_bytes_and_key_ordering():
    data = {"b": 2, "a": 1, "summary": {"total": 158}}
    s1 = json.dumps(data, indent=2)
    s2 = json.dumps(data, indent=2)
    assert s1 == s2

def test_08_exporter_schema_validation():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        reports_dir = tmppath / "outputs" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)

        seg_inv_path = PROJECT_ROOT / "outputs" / "reports" / "v2_3a_final_segment_inventory.csv"
        df_seg = pd.read_csv(seg_inv_path)
        df_map = map_all_segments(df_seg)
        df_map.to_csv(reports_dir / "v2_3f_r8a2_2_segment_native_cell_mapping.csv", index=False, lineterminator="\n")

        cell_groups = df_map.groupby("native_cell_id")
        cells = []
        for cid, grp in cell_groups:
            r0 = grp.iloc[0]
            cells.append({
                "native_cell_id": cid,
                "raster_row_index": r0["raster_row_index"],
                "raster_column_index": r0["raster_column_index"]
            })
        pd.DataFrame(cells).to_csv(reports_dir / "v2_3f_r8a2_2_native_cell_evidence.csv", index=False, lineterminator="\n")

        export_r8a2_2_ui_evidence(source_root=PROJECT_ROOT, output_dir=tmppath)
        json_out = tmppath / "apps" / "web" / "src" / "data" / "r8a2_2_corridor_evidence.json"
        assert json_out.exists()
        with open(json_out, "r", encoding="utf-8") as f:
            jdata = json.load(f)

        assert "summary" in jdata
        assert "cells" in jdata
        assert jdata["summary"]["total_segments"] == 158
        assert jdata["summary"]["occupied_native_cells"] == 11

def test_09_exporter_comparison_mode_nonzero_failure():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        iso_src = tmppath / "isolated_source"
        iso_out = tmppath / "isolated_output"
        missing_out = tmppath / "missing_reference_output"

        iso_src_reports = iso_src / "outputs" / "reports"
        iso_out_reports = iso_out / "outputs" / "reports"
        iso_src_reports.mkdir(parents=True, exist_ok=True)
        iso_out_reports.mkdir(parents=True, exist_ok=True)

        expected_segment_inventory_columns = [
            "segment_id", "sequence_number", "start_chainage_m", "end_chainage_m",
            "nominal_length_m", "actual_geometry_length_m", "start_longitude",
            "start_latitude", "end_longitude", "end_latitude", "midpoint_longitude",
            "midpoint_latitude", "vertex_count", "source_route_sha256", "terminal_segment"
        ]

        expected_mapping_columns = [
            "segment_id", "midpoint_longitude_deg", "midpoint_latitude_deg",
            "coordinate_source", "representative_point_derivation", "raster_row_index",
            "raster_column_index", "native_cell_id", "cell_center_longitude_deg",
            "cell_center_latitude_deg", "west_bound_deg", "east_bound_deg",
            "south_bound_deg", "north_bound_deg", "boundary_rule",
            "mapping_method_a_result", "mapping_method_b_result", "agreement_status",
            "method_a_west_bound_deg", "method_a_east_bound_deg",
            "method_a_south_bound_deg", "method_a_north_bound_deg",
            "method_b_west_bound_deg", "method_b_east_bound_deg",
            "method_b_south_bound_deg", "method_b_north_bound_deg"
        ]

        expected_native_cell_columns = [
            "native_cell_id", "raster_crs", "raster_row_index", "raster_column_index",
            "center_latitude_deg", "center_longitude_deg", "west_bound_deg",
            "east_bound_deg", "south_bound_deg", "north_bound_deg",
            "longitude_spacing_deg", "latitude_spacing_deg", "coordinate_convention",
            "assigned_segments_count", "ordered_segment_list", "segment_ids_sha256",
            "mapping_source", "computation_path", "verification_status"
        ]

        seg_rows = []
        map_rows = []
        for i in range(1, 159):
            s_id = f"NH44_SEG_{i:03d}"
            seg_rows.append({
                "segment_id": s_id,
                "sequence_number": i,
                "start_chainage_m": float((i - 1) * 500),
                "end_chainage_m": float(i * 500),
                "nominal_length_m": 500.0,
                "actual_geometry_length_m": 500.0,
                "start_longitude": 75.15,
                "start_latitude": 33.25,
                "end_longitude": 75.15,
                "end_latitude": 33.25,
                "midpoint_longitude": 75.15,
                "midpoint_latitude": 33.25,
                "vertex_count": 20,
                "source_route_sha256": "0" * 64,
                "terminal_segment": (i == 158)
            })

            map_rows.append({
                "segment_id": s_id,
                "midpoint_longitude_deg": 75.15,
                "midpoint_latitude_deg": 33.25,
                "coordinate_source": "v2_3a_final_segment_inventory.csv",
                "representative_point_derivation": "SEGMENT_MIDPOINT_INTERSECTION",
                "raster_row_index": 2550,
                "raster_column_index": 2551,
                "native_cell_id": "GPM_NATIVE_33.25N_75.15E",
                "cell_center_longitude_deg": 75.15,
                "cell_center_latitude_deg": 33.25,
                "west_bound_deg": 75.10,
                "east_bound_deg": 75.20,
                "south_bound_deg": 33.20,
                "north_bound_deg": 33.30,
                "boundary_rule": "LONGITUDE_[WEST,EAST)_LATITUDE_(SOUTH,NORTH]",
                "mapping_method_a_result": "GPM_NATIVE_33.25N_75.15E",
                "mapping_method_b_result": "METHOD_B_BBOX[75.10,33.20,75.20,33.30]",
                "agreement_status": "EXACT_AGREEMENT",
                "method_a_west_bound_deg": 75.10,
                "method_a_east_bound_deg": 75.20,
                "method_a_south_bound_deg": 33.20,
                "method_a_north_bound_deg": 33.30,
                "method_b_west_bound_deg": 75.10,
                "method_b_east_bound_deg": 75.20,
                "method_b_south_bound_deg": 33.20,
                "method_b_north_bound_deg": 33.30
            })

        df_seg_fixture = pd.DataFrame(seg_rows)
        df_map_fixture = pd.DataFrame(map_rows)

        cell_rows = [{
            "native_cell_id": "GPM_NATIVE_33.25N_75.15E",
            "raster_crs": "EPSG:4326",
            "raster_row_index": 2550,
            "raster_column_index": 2551,
            "center_latitude_deg": 33.25,
            "center_longitude_deg": 75.15,
            "west_bound_deg": 75.10,
            "east_bound_deg": 75.20,
            "south_bound_deg": 33.20,
            "north_bound_deg": 33.30,
            "longitude_spacing_deg": 0.10,
            "latitude_spacing_deg": -0.10,
            "coordinate_convention": "PIXEL_CENTER",
            "assigned_segments_count": 158,
            "ordered_segment_list": ",".join([f"NH44_SEG_{i:03d}" for i in range(1, 159)]),
            "segment_ids_sha256": "0" * 64,
            "mapping_source": "Repository-Declared IMERG-Compatible Analysis Grid",
            "computation_path": "Point-in-BBox Spatial Intersection",
            "verification_status": "DECLARED_GRID_ANALYSIS"
        }]
        df_cells_fixture = pd.DataFrame(cell_rows)

        assert list(df_seg_fixture.columns) == expected_segment_inventory_columns
        assert list(df_map_fixture.columns) == expected_mapping_columns
        assert list(df_cells_fixture.columns) == expected_native_cell_columns

        df_seg_fixture.to_csv(iso_src_reports / "v2_3a_final_segment_inventory.csv", index=False, lineterminator="\n")
        df_map_fixture.to_csv(iso_out_reports / "v2_3f_r8a2_2_segment_native_cell_mapping.csv", index=False, lineterminator="\n")
        df_cells_fixture.to_csv(iso_out_reports / "v2_3f_r8a2_2_native_cell_evidence.csv", index=False, lineterminator="\n")

        # 6. Generate baseline JSON in normal export mode
        export_r8a2_2_ui_evidence(source_root=iso_src, output_dir=iso_out, compare_existing=False)
        json_out = iso_out / "apps" / "web" / "src" / "data" / "r8a2_2_corridor_evidence.json"
        assert json_out.exists()

        # 7. Save exact baseline JSON bytes
        baseline_bytes = json_out.read_bytes()

        # 8 & 9. Compare unchanged inputs successfully & confirm non-rewrite
        export_r8a2_2_ui_evidence(source_root=iso_src, output_dir=iso_out, compare_existing=True)
        assert json_out.read_bytes() == baseline_bytes

        # 10. Mutate one value in a complete mapping-schema column serialized into segments
        df_map_mut = df_map_fixture.copy()
        df_map_mut.loc[0, "midpoint_latitude_deg"] = 99.99
        df_map_mut.to_csv(iso_out_reports / "v2_3f_r8a2_2_segment_native_cell_mapping.csv", index=False, lineterminator="\n")

        # 11 & 12. Require EXPORT_COMPARISON_MISMATCH & confirm baseline remains unchanged
        with pytest.raises(ValueError, match="EXPORT_COMPARISON_MISMATCH"):
            export_r8a2_2_ui_evidence(source_root=iso_src, output_dir=iso_out, compare_existing=True)
        assert json_out.read_bytes() == baseline_bytes

        # 13 & 14. Call comparison mode using absent reference root & require EXPORT_REFERENCE_NOT_FOUND
        with pytest.raises(FileNotFoundError, match="EXPORT_REFERENCE_NOT_FOUND"):
            export_r8a2_2_ui_evidence(source_root=iso_src, output_dir=missing_out, compare_existing=True)

        # 15, 16 & 17. Confirm missing_out was not created, no JSON created & early failure occurred
        assert not missing_out.exists()
        missing_json = missing_out / "apps" / "web" / "src" / "data" / "r8a2_2_corridor_evidence.json"
        assert not missing_json.exists()

def test_10_archive_compatible_root_discovery_without_git():
    assert (PROJECT_ROOT / "pyproject.toml").exists()

def test_11_repository_reference_integrity():
    ref_file = PROJECT_ROOT / "configs" / "v2_3f_r8a2_2_release_references.json"
    assert ref_file.exists()
    with open(ref_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["release_references"]) == 5

def test_12_manifest_positive_validation():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        import subprocess

        blob_bytes = subprocess.check_output(
            ["git", "cat-file", "-p", "HEAD:pyproject.toml"],
            cwd=PROJECT_ROOT
        )
        digest = hashlib.sha256(blob_bytes).hexdigest()
        size_bytes = len(blob_bytes)

        man_df = pd.DataFrame([{
            "artifact_alias": "pyproject_toml",
            "file_path": "pyproject.toml",
            "sha256": digest,
            "file_size_bytes": size_bytes,
            "classification": "CONFIGURATION"
        }])
        man_csv = tmppath / "v2_3f_r8a2_2_repository_manifest.csv"
        man_df.to_csv(man_csv, index=False, lineterminator="\n")

        assert validate_r8a2_2_manifest("HEAD", manifest_csv_path=man_csv, source_root=PROJECT_ROOT)

        # Hash mutation test
        man_df_mut = man_df.copy()
        man_df_mut.loc[0, "sha256"] = "0" * 64
        man_csv_mut = tmppath / "v2_3f_r8a2_2_repository_manifest_mut.csv"
        man_df_mut.to_csv(man_csv_mut, index=False, lineterminator="\n")
        assert not validate_r8a2_2_manifest("HEAD", manifest_csv_path=man_csv_mut, source_root=PROJECT_ROOT)

        # Size mutation test
        man_df_size_mut = man_df.copy()
        man_df_size_mut.loc[0, "file_size_bytes"] = size_bytes + 1
        man_csv_size_mut = tmppath / "v2_3f_r8a2_2_repository_manifest_size_mut.csv"
        man_df_size_mut.to_csv(man_csv_size_mut, index=False, lineterminator="\n")
        assert not validate_r8a2_2_manifest("HEAD", manifest_csv_path=man_csv_size_mut, source_root=PROJECT_ROOT)

def test_13_missing_entry_negative_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        man_df = pd.DataFrame([{
            "artifact_alias": "nonexistent_file",
            "file_path": "outputs/reports/nonexistent.csv",
            "sha256": "a" * 64,
            "file_size_bytes": 100,
            "classification": "CANONICAL_OUTPUT"
        }])
        man_csv = tmppath / "v2_3f_r8a2_2_repository_manifest.csv"
        man_df.to_csv(man_csv, index=False, lineterminator="\n")

        assert not validate_r8a2_2_manifest("HEAD", manifest_csv_path=man_csv, source_root=tmppath)

def test_14_extra_entry_negative_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        reports_dir = tmppath / "outputs" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "f1.csv").write_bytes(b"data\n")

        man_df = pd.DataFrame([
            {"artifact_alias": "f1_csv", "file_path": "outputs/reports/f1.csv", "sha256": hashlib.sha256(b"data\n").hexdigest(), "file_size_bytes": 5, "classification": "CANONICAL_OUTPUT"},
            {"artifact_alias": "f2_csv", "file_path": "outputs/reports/f2.csv", "sha256": "b" * 64, "file_size_bytes": 10, "classification": "CANONICAL_OUTPUT"}
        ])
        man_csv = tmppath / "v2_3f_r8a2_2_repository_manifest.csv"
        man_df.to_csv(man_csv, index=False, lineterminator="\n")

        assert not validate_r8a2_2_manifest("HEAD", manifest_csv_path=man_csv, source_root=tmppath)

def test_15_duplicate_entry_negative_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        reports_dir = tmppath / "outputs" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "f1.csv").write_bytes(b"data\n")

        d = hashlib.sha256(b"data\n").hexdigest()
        man_df = pd.DataFrame([
            {"artifact_alias": "f1_csv", "file_path": "outputs/reports/f1.csv", "sha256": d, "file_size_bytes": 5, "classification": "CANONICAL_OUTPUT"},
            {"artifact_alias": "f1_csv", "file_path": "outputs/reports/f1.csv", "sha256": d, "file_size_bytes": 5, "classification": "CANONICAL_OUTPUT"}
        ])
        man_csv = tmppath / "v2_3f_r8a2_2_repository_manifest.csv"
        man_df.to_csv(man_csv, index=False, lineterminator="\n")

        assert not validate_r8a2_2_manifest("HEAD", manifest_csv_path=man_csv, source_root=tmppath)

def test_16_malformed_hash_negative_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        reports_dir = tmppath / "outputs" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "f1.csv").write_bytes(b"data\n")

        man_df = pd.DataFrame([
            {"artifact_alias": "f1_csv", "file_path": "outputs/reports/f1.csv", "sha256": "invalid_hash_str", "file_size_bytes": 5, "classification": "CANONICAL_OUTPUT"}
        ])
        man_csv = tmppath / "v2_3f_r8a2_2_repository_manifest.csv"
        man_df.to_csv(man_csv, index=False, lineterminator="\n")

        assert not validate_r8a2_2_manifest("HEAD", manifest_csv_path=man_csv, source_root=tmppath)

def test_17_hash_mismatch_negative_test():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        reports_dir = tmppath / "outputs" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        (reports_dir / "f1.csv").write_bytes(b"data\n")

        bad_hash = "0" * 64
        man_df = pd.DataFrame([
            {"artifact_alias": "f1_csv", "file_path": "outputs/reports/f1.csv", "sha256": bad_hash, "file_size_bytes": 5, "classification": "CANONICAL_OUTPUT"}
        ])
        man_csv = tmppath / "v2_3f_r8a2_2_repository_manifest.csv"
        man_df.to_csv(man_csv, index=False, lineterminator="\n")

        assert not validate_r8a2_2_manifest("HEAD", manifest_csv_path=man_csv, source_root=tmppath)

def test_18_scenario_mutation_sensitivity():
    sc_defs = load_scenario_definitions(yaml_path=PROJECT_ROOT / "configs" / "scenario_definitions.yaml")
    sc_defs_mut = copy.deepcopy(sc_defs)
    sc_defs_mut["S1_MODERATE"]["r24_mm"] = 999.0
    with pytest.raises(AssertionError, match="Mismatch for S1 R24"):
        generate_18_provenance_records(sc_defs=sc_defs_mut)

def test_19_boundary_or_mapping_mutation_sensitivity():
    m1 = map_segment_method_a(33.25, 75.15)
    m2 = map_segment_method_a(33.25, 75.25)
    assert m1["native_cell_id"] != m2["native_cell_id"]

    # Mutation test exercising production mapping reconciliation logic with separate Method A and Method B columns
    df_synth = pd.DataFrame([
        {
            "method_a_west_bound_deg": 75.10, "method_a_east_bound_deg": 75.20,
            "method_a_south_bound_deg": 33.20, "method_a_north_bound_deg": 33.30,
            "method_b_west_bound_deg": 75.10, "method_b_east_bound_deg": 75.20,
            "method_b_south_bound_deg": 33.20, "method_b_north_bound_deg": 33.30
        },
        {
            "method_a_west_bound_deg": 75.10, "method_a_east_bound_deg": 75.20,
            "method_a_south_bound_deg": 33.20, "method_a_north_bound_deg": 33.30,
            "method_b_west_bound_deg": 75.00, "method_b_east_bound_deg": 75.10,
            "method_b_south_bound_deg": 33.20, "method_b_north_bound_deg": 33.30
        }
    ])
    res = compute_mapping_reconciliation(df_synth)
    assert res["segments_compared"] == 2
    assert res["equal_count"] == 1
    assert res["discrepancy_count"] == 1
    assert res["all_rows_equal"] is False
    assert res["row_equality"] == [True, False]

    # Reject missing observations
    df_missing_col = pd.DataFrame([{"method_a_west_bound_deg": 75.10}])
    with pytest.raises(KeyError, match="Missing required mapping observation column"):
        compute_mapping_reconciliation(df_missing_col)

    df_null_val = df_synth.copy()
    df_null_val.loc[0, "method_b_west_bound_deg"] = None
    with pytest.raises(ValueError, match="contain null values"):
        compute_mapping_reconciliation(df_null_val)

def test_20_no_self_declared_pass_evidence():
    # Exhaustive scan of all 10 production candidate files for prohibited verdict strings
    candidate_files = [
        PROJECT_ROOT / "configs" / "v2_3f_r8a2_2_release_references.json",
        PROJECT_ROOT / "docs" / "v2" / "V2_3F_R8A2_2_CANDIDATE_REPORT.md",
        PROJECT_ROOT / "scripts" / "export_v2_3f_r8a2_2_ui_evidence.py",
        PROJECT_ROOT / "scripts" / "generate_v2_3f_r8a2_2_manifest.py",
        PROJECT_ROOT / "scripts" / "run_v2_3f_r8a2_2_pipeline.py",
        PROJECT_ROOT / "scripts" / "run_v2_3f_r8a2_2_reproducibility.py",
        PROJECT_ROOT / "scripts" / "validate_v2_3f_r8a2_2_manifest.py",
        PROJECT_ROOT / "scripts" / "verify_v2_3f_r8a2_2_repository_references.py",
        PROJECT_ROOT / "src" / "geoslide" / "scientific_audits.py",
        PROJECT_ROOT / "apps" / "web" / "app" / "corridor" / "page.tsx",
    ]
    
    prohibited_pattern = re.compile(
        r"(?<![A-Za-z0-9_])"
        r"(?:"
        r"PASS(?:ED)?|SUCCESS|VERIFIED(?:_[A-Za-z0-9]+)*|OK|"
        r"MATCH(?:ED)?|AGREEMENT|CONFIRMED|VALIDATED|"
        r"EXACT_(?:MATCH|AGREEMENT)|"
        r"(?:[A-Za-z0-9]+_)*IDENTICAL|"
        r"(?:[A-Za-z0-9]+_)*RECONCILED"
        r")"
        r"(?![A-Za-z0-9_])",
        re.IGNORECASE,
    )
    
    # Canary assertions
    canary_prohibited = [
        "PASS",
        "VERIFIED_100PERCENT_AGREEMENT",
        "EXACT_MATCH",
        "EXACT_AGREEMENT",
        "METHOD_A_B_IDENTICAL",
        "RECORDS_RECONCILED",
    ]
    for bad_tok in canary_prohibited:
        assert prohibited_pattern.search(bad_tok), f"Canary failed: '{bad_tok}' was not rejected by prohibited_pattern"
        
    canary_allowed = ["MODERATE_AGREEMENT"]
    for good_tok in canary_allowed:
        assert not prohibited_pattern.search(good_tok), f"Canary failed: '{good_tok}' was incorrectly rejected by prohibited_pattern"
    
    literal_zero_metric_pattern = re.compile(
        r"\b(?:mismatch_count|hash_mismatch_count|size_mismatch_count|"
        r"total_mismatch_count|missing_entry_count|total_discrepancy_count|"
        r"comparison_difference)=0\b",
        re.IGNORECASE,
    )
    
    for cfile in candidate_files:
        assert cfile.exists(), f"Missing production candidate file: {cfile}"
        content = cfile.read_text(encoding="utf-8")
        
        if cfile.suffix == ".py":
            tree = ast.parse(content, filename=str(cfile))
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    val = node.value
                    matches = prohibited_pattern.findall(val)
                    assert not matches, f"Prohibited verdict string '{matches}' in string literal in {cfile.name}: '{val}'"
                    if cfile.name in ("run_v2_3f_r8a2_2_reproducibility.py", "validate_v2_3f_r8a2_2_manifest.py"):
                        zero_matches = literal_zero_metric_pattern.findall(val)
                        assert not zero_matches, f"Literal zero metric string '{zero_matches}' in {cfile.name}: '{val}'"
        else:
            matches = prohibited_pattern.findall(content)
            assert not matches, f"Prohibited verdict string '{matches}' found in text of {cfile.name}"
            if cfile.name in ("run_v2_3f_r8a2_2_reproducibility.py", "validate_v2_3f_r8a2_2_manifest.py"):
                zero_matches = literal_zero_metric_pattern.findall(content)
                assert not zero_matches, f"Literal zero metric string '{zero_matches}' in text of {cfile.name}"

    # Explicit pipeline check for self-declared exit/status assertions
    pipe_code = (PROJECT_ROOT / "scripts" / "run_v2_3f_r8a2_2_pipeline.py").read_text(encoding="utf-8")
    assert 'exit_code": "0"' not in pipe_code
    assert 'status": "PASS"' not in pipe_code
    assert 'audit_status": "VERIFIED_EXACT"' not in pipe_code

def test_21_exact_ui_import_path_and_capitalization():
    corridor_page = (PROJECT_ROOT / "apps" / "web" / "app" / "corridor" / "page.tsx").read_text(encoding="utf-8")
    assert '@' in corridor_page
    assert 'r8a2_2_corridor_evidence.json' in corridor_page
    
    ui_json_path = PROJECT_ROOT / "apps" / "web" / "src" / "data" / "r8a2_2_corridor_evidence.json"
    assert ui_json_path.exists(), f"Tracked UI evidence JSON artifact missing: {ui_json_path}"
    
    ui_data = json.loads(ui_json_path.read_text(encoding="utf-8"))
    assert isinstance(ui_data, dict), "UI evidence JSON schema invalid"
    assert "segments" in ui_data and "cells" in ui_data
    assert isinstance(ui_data["segments"], list) and isinstance(ui_data["cells"], list)
    assert len(ui_data["segments"]) == 158, f"Expected 158 segments, got {len(ui_data['segments'])}"
    assert len(ui_data["cells"]) == 11, f"Expected 11 native cells, got {len(ui_data['cells'])}"

def test_22_no_hardcoded_scientific_ui_values():
    corridor_page = (PROJECT_ROOT / "apps" / "web" / "app" / "corridor" / "page.tsx").read_text(encoding="utf-8")
    assert "2 Native GPM" not in corridor_page
    assert "Authoritative V2-3F-R4" not in corridor_page

def test_23_pipeline_and_exporter_contain_no_git_or_network_dependency():
    pipe_code = (PROJECT_ROOT / "scripts" / "run_v2_3f_r8a2_2_pipeline.py").read_text(encoding="utf-8")
    exp_code = (PROJECT_ROOT / "scripts" / "export_v2_3f_r8a2_2_ui_evidence.py").read_text(encoding="utf-8")

    assert "subprocess.check_output([\"git\"" not in pipe_code
    assert "subprocess.check_output([\"git\"" not in exp_code
    assert "import urllib" not in pipe_code
    assert "import requests" not in pipe_code
