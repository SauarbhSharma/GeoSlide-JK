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

class TestNH44PlaceAnchor(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.audit_dir = self.project_root / "data" / "audit"
        self.reports_dir = self.project_root / "outputs" / "reports"
        self.docs_dir = self.project_root / "docs" / "v2"

    def test_v2_3a_2g_documentation_and_reports_exist(self):
        self.assertTrue((self.docs_dir / "V2_3A_2G_OSM_RELATION_AUDIT.md").exists())
        self.assertTrue((self.docs_dir / "V2_3A_2G_COMPLETION_REPORT.md").exists())
        self.assertTrue((self.audit_dir / "nh44_place_reference_points.csv").exists())
        self.assertTrue((self.audit_dir / "nh44_place_reference_points.geojson").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2g_place_projection.csv").exists())
        self.assertTrue((self.audit_dir / "nh44_place_route_projections.geojson").exists())
        self.assertTrue((self.reports_dir / "v2_3a_2g_osm_relation_edge_match.csv").exists())

    def test_place_references_have_osm_ids(self):
        df_places = pd.read_csv(self.audit_dir / "nh44_place_reference_points.csv")
        self.assertEqual(len(df_places), 7, "Must contain exactly 7 place reference points!")
        self.assertTrue((df_places['osm_id'] > 0).all(), "All place references must have valid OSM IDs!")

    def test_projected_points_lie_on_route(self):
        df_proj = pd.read_csv(self.reports_dir / "v2_3a_2g_place_projection.csv")
        max_dist = df_proj['projected_marker_on_route_distance_m'].max()
        self.assertLessEqual(max_dist, 0.01, f"Projected markers must lie <= 0.01m from route! Max: {max_dist}")

    def test_monotonic_place_chainage_order(self):
        df_proj = pd.read_csv(self.reports_dir / "v2_3a_2g_place_projection.csv")
        df_mon = df_proj[df_proj["place_name"].isin(["Udhampur", "Chenani", "Ramban", "Ramsoo", "Banihal"])].sort_values("chainage_km")
        chainages = list(df_mon["chainage_km"])
        is_increasing = all(x < y for x, y in zip(chainages, chainages[1:]))
        self.assertTrue(is_increasing, f"Place chainages must be strictly monotonic! Values: {chainages}")

    def test_rejected_endpoint_is_not_banihal(self):
        rej_lon, rej_lat = 75.186696, 33.564998
        banihal_dist_km = haversine_distance(rej_lon, rej_lat, 75.204000, 33.438000) / 1000.0
        self.assertGreater(banihal_dist_km, 14.0, f"Rejected 33.5650°N endpoint is {banihal_dist_km:.1f} km past Banihal and must not be called Banihal!")

if __name__ == "__main__":
    unittest.main()
