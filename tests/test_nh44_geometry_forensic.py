import unittest
import os, math
import pandas as pd
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Point

def haversine_distance(lon1, lat1, lon2, lat2):
    R = 6371000.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class TestNH44GeometryForensic(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"

    def test_v2_3a_2f_documentation_and_reports_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_2F_REJECTED_TERMINAL_LOCK.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2F_GEOMETRY_FORENSIC_REPORT.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2F_COMPLETION_REPORT.md").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2f_geometry_inventory.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2f_coordinate_samples.csv").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2f_source_fidelity.csv").exists())
        self.assertTrue((self.audit_dir / "nh44_forensic_vertex_traceability.csv").exists())

    def test_route_length_geodesic_invariant(self):
        val_path = self.audit_dir / "nh44_repaired_mainline_validation.geojson"
        self.assertTrue(val_path.exists())
        gdf_val = gpd.read_file(val_path)
        val_g_4326 = gdf_val.geometry.iloc[0]
        val_g_utm = gdf_val.to_crs('EPSG:32643').geometry.iloc[0]

        sub_geoms = []
        if val_g_4326.geom_type == 'LineString': sub_geoms.append(val_g_4326)
        elif val_g_4326.geom_type == 'MultiLineString': sub_geoms.extend(list(val_g_4326.geoms))

        s_coords = list(sub_geoms[0].coords)
        n_coords = list(sub_geoms[-1].coords)

        s_lon, s_lat = s_coords[0][0], s_coords[0][1]
        n_lon, n_lat = n_coords[-1][0], n_coords[-1][1]

        route_len_km = val_g_utm.length / 1000.0
        geodesic_dist_km = haversine_distance(s_lon, s_lat, n_lon, n_lat) / 1000.0

        self.assertGreaterEqual(route_len_km, geodesic_dist_km, 
            f"Route length ({route_len_km:.2f} km) must be >= geodesic distance ({geodesic_dist_km:.2f} km)")

    def test_geographic_latitude_order(self):
        val_path = self.audit_dir / "nh44_repaired_mainline_validation.geojson"
        gdf_val = gpd.read_file(val_path)
        val_g_4326 = gdf_val.geometry.iloc[0]

        sub_geoms = []
        if val_g_4326.geom_type == 'LineString': sub_geoms.append(val_g_4326)
        elif val_g_4326.geom_type == 'MultiLineString': sub_geoms.extend(list(val_g_4326.geoms))

        s_lat = sub_geoms[0].coords[0][1]
        n_lat = sub_geoms[-1].coords[-1][1]

        self.assertLess(s_lat, n_lat, f"Udhampur lat ({s_lat:.4f}) must be less than Banihal lat ({n_lat:.4f})")

    def test_longitude_range_not_collapsed(self):
        val_path = self.audit_dir / "nh44_repaired_mainline_validation.geojson"
        gdf_val = gpd.read_file(val_path)
        b = gdf_val.total_bounds # [minx, miny, maxx, maxy]
        lon_range = b[2] - b[0]

        self.assertGreater(lon_range, 0.05, f"Longitude range ({lon_range:.4f}°) must not be collapsed to straight line!")

    def test_synthetic_vertices_count_zero(self):
        fid_csv = self.reports_dir / "v2_3a_2f_source_fidelity.csv"
        df_fid = pd.read_csv(fid_csv)
        synth_cnt = df_fid['synthetic_vertices_count'].iloc[0]

        self.assertEqual(synth_cnt, 0, "Synthetic vertices count must be zero!")

if __name__ == "__main__":
    unittest.main()
