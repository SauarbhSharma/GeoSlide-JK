"""
GeoSlide-JK 2.0 — Canonical Boundary & Two-Method Grid Spatial Mapper
Implements Method A (Exact Rational/Decimal Inverse Grid Indexing) and
Method B (Independent Polygon BBox Point-in-Cell Spatial Construction)
Enforces canonical boundary rules: Longitude [west, east) and Latitude (south, north].
"""

import math
from decimal import Decimal
import pandas as pd
import numpy as np

def map_segment_method_a(lat, lon):
    """
    Method A: Exact decimal/rational inverse-grid indexing without floating-point floor ambiguity.
    Grid affine: Affine(0.1, 0.0, -180.0, 0.0, -0.1, 90.0)
    """
    d_lat = Decimal(str(lat))
    d_lon = Decimal(str(lon))
    
    col = int(math.floor((d_lon - Decimal("-180.0")) / Decimal("0.1")))
    row = int(math.floor((Decimal("90.0") - d_lat) / Decimal("0.1")))
    
    west = float(Decimal("-180.0") + Decimal(col) * Decimal("0.1"))
    east = float(Decimal(str(west)) + Decimal("0.1"))
    north = float(Decimal("90.0") - Decimal(row) * Decimal("0.1"))
    south = float(Decimal(str(north)) - Decimal("0.1"))
    
    lon_c = float(Decimal(str(west)) + Decimal("0.05"))
    lat_c = float(Decimal(str(south)) + Decimal("0.05"))
    
    res_str = f"METHOD_A_CELL_{lat_c:.2f}N_{lon_c:.2f}E_row{row}_col{col}"
    
    return {
        "row": row,
        "col": col,
        "west": round(west, 2),
        "east": round(east, 2),
        "south": round(south, 2),
        "north": round(north, 2),
        "lon_center": round(lon_c, 2),
        "lat_center": round(lat_c, 2),
        "result_str": res_str,
        "native_cell_id": f"GPM_NATIVE_{lat_c:.2f}N_{lon_c:.2f}E"
    }

def map_segment_method_b(lat, lon):
    """
    Method B: Independent candidate cell polygon BBox spatial construction.
    Does NOT call Method A or reuse Method A row, column, cell ID or bounds.
    Applies boundary rules: west <= lon < east AND south < lat <= north
    """
    d_lat = Decimal(str(lat))
    d_lon = Decimal(str(lon))
    
    # Construct candidate BBoxes around the point
    b_lon_base = math.floor(float(d_lon) * 10) / 10.0
    b_lat_base = math.floor(float(d_lat) * 10) / 10.0
    
    # Search candidates in grid neighbourhood
    candidate_lons = [round(b_lon_base - 0.1, 2), round(b_lon_base, 2), round(b_lon_base + 0.1, 2)]
    candidate_lats = [round(b_lat_base - 0.1, 2), round(b_lat_base, 2), round(b_lat_base + 0.1, 2)]
    
    matched_bbox = None
    for c_west in candidate_lons:
        c_east = round(c_west + 0.1, 2)
        for c_south in candidate_lats:
            c_north = round(c_south + 0.1, 2)
            
            # Canonical boundary test: [west, east) and (south, north]
            d_c_west = Decimal(str(c_west))
            d_c_east = Decimal(str(c_east))
            d_c_south = Decimal(str(c_south))
            d_c_north = Decimal(str(c_north))
            
            in_lon = (d_c_west <= d_lon < d_c_east)
            in_lat = (d_c_south < d_lat <= d_c_north)
            
            if in_lon and in_lat:
                matched_bbox = (c_west, c_south, c_east, c_north)
                break
        if matched_bbox:
            break
            
    assert matched_bbox is not None, f"No Method B BBox matched point ({lat}, {lon})"
    
    b_west, b_south, b_east, b_north = matched_bbox
    res_str = f"METHOD_B_BBOX[{b_west:.2f},{b_south:.2f},{b_east:.2f},{b_north:.2f}]"
    
    return {
        "west": b_west,
        "east": b_east,
        "south": b_south,
        "north": b_north,
        "result_str": res_str
    }

def map_all_segments(df_seg):
    """
    Maps all 158 corridor segments using Method A and Method B independently.
    """
    rows = []
    for _, r in df_seg.iterrows():
        seg_id = r["segment_id"]
        lat = float(r["midpoint_latitude"])
        lon = float(r["midpoint_longitude"])
        
        mA = map_segment_method_a(lat, lon)
        mB = map_segment_method_b(lat, lon)
        
        # Reconciliation check
        exact_match = (
            mA["west"] == mB["west"] and
            mA["east"] == mB["east"] and
            mA["south"] == mB["south"] and
            mA["north"] == mB["north"]
        )
        agreement = "EXACT_AGREEMENT" if exact_match else "DISCREPANCY"
        
        rows.append({
            "segment_id": seg_id,
            "midpoint_longitude_deg": lon,
            "midpoint_latitude_deg": lat,
            "coordinate_source": "v2_3a_final_segment_inventory.csv",
            "representative_point_derivation": "SEGMENT_MIDPOINT_INTERSECTION",
            "raster_row_index": mA["row"],
            "raster_column_index": mA["col"],
            "native_cell_id": mA["native_cell_id"],
            "cell_center_longitude_deg": mA["lon_center"],
            "cell_center_latitude_deg": mA["lat_center"],
            "west_bound_deg": mA["west"],
            "east_bound_deg": mA["east"],
            "south_bound_deg": mA["south"],
            "north_bound_deg": mA["north"],
            "boundary_rule": "LONGITUDE_[WEST,EAST)_LATITUDE_(SOUTH,NORTH]",
            "mapping_method_a_result": mA["result_str"],
            "mapping_method_b_result": mB["result_str"],
            "agreement_status": agreement
        })
        
    return pd.DataFrame(rows)
