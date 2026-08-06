# GeoSlide-JK 2.0 — V2-3B Segment Feature Data Dictionary

> **Total Extracted Feature Columns:** 92  
> **Row Count:** 158 Authoritative Segments

---

## Extracted Feature Columns Summary

| Column Name | Category | Data Type | Units | Description |
| :--- | :--- | :--- | :--- | :--- |
| `segment_id` | Identification | `str` | metres | Extracted static geospatial metric: segment id across 100m segment buffer. |
| `segment_index` | Identification | `int64` | metres | Extracted static geospatial metric: segment index across 100m segment buffer. |
| `chainage_start_m` | Identification | `float64` | metres | Extracted static geospatial metric: chainage start m across 100m segment buffer. |
| `chainage_end_m` | Identification | `float64` | metres | Extracted static geospatial metric: chainage end m across 100m segment buffer. |
| `chainage_mid_m` | Identification | `float64` | metres | Extracted static geospatial metric: chainage mid m across 100m segment buffer. |
| `length_m` | Identification | `float64` | metres | Extracted static geospatial metric: length m across 100m segment buffer. |
| `is_residual_segment` | Identification | `bool` | metres | Extracted static geospatial metric: is residual segment across 100m segment buffer. |
| `start_longitude` | Identification | `float64` | count / text | Extracted static geospatial metric: start longitude across 100m segment buffer. |
| `start_latitude` | Identification | `float64` | count / text | Extracted static geospatial metric: start latitude across 100m segment buffer. |
| `end_longitude` | Identification | `float64` | count / text | Extracted static geospatial metric: end longitude across 100m segment buffer. |
| `end_latitude` | Identification | `float64` | count / text | Extracted static geospatial metric: end latitude across 100m segment buffer. |
| `midpoint_longitude` | Identification | `float64` | metres | Extracted static geospatial metric: midpoint longitude across 100m segment buffer. |
| `midpoint_latitude` | Identification | `float64` | metres | Extracted static geospatial metric: midpoint latitude across 100m segment buffer. |
| `district_name` | Identification | `str` | metres | Extracted static geospatial metric: district name across 100m segment buffer. |
| `analysis_buffer_m` | Identification | `int64` | metres | Extracted static geospatial metric: analysis buffer m across 100m segment buffer. |
| `elevation_min_m` | Terrain | `object` | metres | Extracted static geospatial metric: elevation min m across 100m segment buffer. |
| `elevation_max_m` | Terrain | `object` | metres | Extracted static geospatial metric: elevation max m across 100m segment buffer. |
| `elevation_mean_m` | Terrain | `object` | metres | Extracted static geospatial metric: elevation mean m across 100m segment buffer. |
| `elevation_median_m` | Terrain | `object` | metres | Extracted static geospatial metric: elevation median m across 100m segment buffer. |
| `elevation_std_m` | Terrain | `object` | metres | Extracted static geospatial metric: elevation std m across 100m segment buffer. |
| `elevation_range_m` | Terrain | `object` | metres | Extracted static geospatial metric: elevation range m across 100m segment buffer. |
| `elevation_p90_m` | Terrain | `object` | metres | Extracted static geospatial metric: elevation p90 m across 100m segment buffer. |
| `slope_min_deg` | Terrain | `object` | metres | Extracted static geospatial metric: slope min deg across 100m segment buffer. |
| `slope_max_deg` | Terrain | `object` | metres | Extracted static geospatial metric: slope max deg across 100m segment buffer. |
| `slope_mean_deg` | Terrain | `object` | metres | Extracted static geospatial metric: slope mean deg across 100m segment buffer. |
| `slope_median_deg` | Terrain | `object` | metres | Extracted static geospatial metric: slope median deg across 100m segment buffer. |
| `slope_std_deg` | Terrain | `object` | degrees | Extracted static geospatial metric: slope std deg across 100m segment buffer. |
| `slope_p90_deg` | Terrain | `object` | degrees | Extracted static geospatial metric: slope p90 deg across 100m segment buffer. |
| `slope_pct_above_15deg` | Terrain | `object` | degrees | Extracted static geospatial metric: slope pct above 15deg across 100m segment buffer. |
| `slope_pct_above_25deg` | Terrain | `object` | degrees | Extracted static geospatial metric: slope pct above 25deg across 100m segment buffer. |
| `slope_pct_above_35deg` | Terrain | `object` | degrees | Extracted static geospatial metric: slope pct above 35deg across 100m segment buffer. |
| `aspect_circular_mean_deg` | Terrain | `object` | metres | Extracted static geospatial metric: aspect circular mean deg across 100m segment buffer. |
| `aspect_north_fraction` | Terrain | `object` | fraction [0-1] | Extracted static geospatial metric: aspect north fraction across 100m segment buffer. |
| `aspect_east_fraction` | Terrain | `object` | fraction [0-1] | Extracted static geospatial metric: aspect east fraction across 100m segment buffer. |
| `aspect_south_fraction` | Terrain | `object` | fraction [0-1] | Extracted static geospatial metric: aspect south fraction across 100m segment buffer. |
| `aspect_west_fraction` | Terrain | `object` | fraction [0-1] | Extracted static geospatial metric: aspect west fraction across 100m segment buffer. |
| `aspect_dominant_class` | Terrain | `object` | metres | Extracted static geospatial metric: aspect dominant class across 100m segment buffer. |
| `hillshade_mean` | Terrain | `object` | metres | Extracted static geospatial metric: hillshade mean across 100m segment buffer. |
| `hillshade_median` | Terrain | `object` | metres | Extracted static geospatial metric: hillshade median across 100m segment buffer. |
| `hillshade_std` | Terrain | `object` | count / text | Extracted static geospatial metric: hillshade std across 100m segment buffer. |
| `susceptibility_min_prob` | Susceptibility | `object` | metres | Extracted static geospatial metric: susceptibility min prob across 100m segment buffer. |
| `susceptibility_max_prob` | Susceptibility | `object` | metres | Extracted static geospatial metric: susceptibility max prob across 100m segment buffer. |
| `susceptibility_mean_prob` | Susceptibility | `object` | metres | Extracted static geospatial metric: susceptibility mean prob across 100m segment buffer. |
| `susceptibility_median_prob` | Susceptibility | `object` | metres | Extracted static geospatial metric: susceptibility median prob across 100m segment buffer. |
| `susceptibility_std_prob` | Susceptibility | `object` | count / text | Extracted static geospatial metric: susceptibility std prob across 100m segment buffer. |
| `susceptibility_p75_prob` | Susceptibility | `object` | count / text | Extracted static geospatial metric: susceptibility p75 prob across 100m segment buffer. |
| `susceptibility_p90_prob` | Susceptibility | `object` | count / text | Extracted static geospatial metric: susceptibility p90 prob across 100m segment buffer. |
| `susceptibility_p95_prob` | Susceptibility | `object` | count / text | Extracted static geospatial metric: susceptibility p95 prob across 100m segment buffer. |
| `susceptibility_very_low_fraction` | Susceptibility | `object` | fraction [0-1] | Extracted static geospatial metric: susceptibility very low fraction across 100m segment buffer. |
| `susceptibility_low_fraction` | Susceptibility | `object` | fraction [0-1] | Extracted static geospatial metric: susceptibility low fraction across 100m segment buffer. |
| `susceptibility_moderate_fraction` | Susceptibility | `object` | fraction [0-1] | Extracted static geospatial metric: susceptibility moderate fraction across 100m segment buffer. |
| `susceptibility_high_fraction` | Susceptibility | `object` | fraction [0-1] | Extracted static geospatial metric: susceptibility high fraction across 100m segment buffer. |
| `susceptibility_very_high_fraction` | Susceptibility | `object` | fraction [0-1] | Extracted static geospatial metric: susceptibility very high fraction across 100m segment buffer. |
| `susceptibility_dominant_class` | Susceptibility | `object` | metres | Extracted static geospatial metric: susceptibility dominant class across 100m segment buffer. |
| `susceptibility_pct_high_very_high` | Susceptibility | `object` | percentage | Extracted static geospatial metric: susceptibility pct high very high across 100m segment buffer. |
| `susceptibility_max_contiguous_high_len_m` | Susceptibility | `object` | metres | Extracted static geospatial metric: susceptibility max contiguous high len m across 100m segment buffer. |
| `landcover_dominant_class` | LandCover | `str` | metres | Extracted static geospatial metric: landcover dominant class across 100m segment buffer. |
| `landcover_builtup_fraction` | LandCover | `float64` | fraction [0-1] | Extracted static geospatial metric: landcover builtup fraction across 100m segment buffer. |
| `landcover_cropland_fraction` | LandCover | `float64` | fraction [0-1] | Extracted static geospatial metric: landcover cropland fraction across 100m segment buffer. |
| `landcover_forest_fraction` | LandCover | `float64` | fraction [0-1] | Extracted static geospatial metric: landcover forest fraction across 100m segment buffer. |
| `landcover_grassland_fraction` | LandCover | `float64` | fraction [0-1] | Extracted static geospatial metric: landcover grassland fraction across 100m segment buffer. |
| `landcover_bareground_fraction` | LandCover | `float64` | fraction [0-1] | Extracted static geospatial metric: landcover bareground fraction across 100m segment buffer. |
| `landcover_water_fraction` | LandCover | `float64` | fraction [0-1] | Extracted static geospatial metric: landcover water fraction across 100m segment buffer. |
| `landcover_snow_ice_fraction` | LandCover | `float64` | fraction [0-1] | Extracted static geospatial metric: landcover snow ice fraction across 100m segment buffer. |
| `geology_dominant_lithology` | Geology | `str` | metres | Extracted static geospatial metric: geology dominant lithology across 100m segment buffer. |
| `geology_lithological_diversity_count` | Geology | `int64` | count / text | Extracted static geospatial metric: geology lithological diversity count across 100m segment buffer. |
| `geology_overlap_pct` | Geology | `float64` | percentage | Extracted static geospatial metric: geology overlap pct across 100m segment buffer. |
| `fault_distance_nearest_m` | Geology | `float64` | metres | Extracted static geospatial metric: fault distance nearest m across 100m segment buffer. |
| `fault_intersection_count` | Geology | `int64` | count / text | Extracted static geospatial metric: fault intersection count across 100m segment buffer. |
| `fault_density_100m_m_per_sqkm` | Geology | `float64` | metres | Extracted static geospatial metric: fault density 100m m per sqkm across 100m segment buffer. |
| `fault_density_250m_m_per_sqkm` | Geology | `float64` | metres | Extracted static geospatial metric: fault density 250m m per sqkm across 100m segment buffer. |
| `fault_distance_active_m` | Geology | `float64` | metres | Extracted static geospatial metric: fault distance active m across 100m segment buffer. |
| `fault_active_intersection_count` | Geology | `int64` | count / text | Extracted static geospatial metric: fault active intersection count across 100m segment buffer. |
| `drainage_distance_min_m` | Identification | `float64` | metres | Extracted static geospatial metric: drainage distance min m across 100m segment buffer. |
| `drainage_distance_mean_m` | Identification | `float64` | metres | Extracted static geospatial metric: drainage distance mean m across 100m segment buffer. |
| `drainage_intersection_count` | Identification | `int64` | count / text | Extracted static geospatial metric: drainage intersection count across 100m segment buffer. |
| `drainage_density_100m_m_per_sqkm` | Identification | `float64` | metres | Extracted static geospatial metric: drainage density 100m m per sqkm across 100m segment buffer. |
| `road_distance_min_m` | Identification | `float64` | metres | Extracted static geospatial metric: road distance min m across 100m segment buffer. |
| `road_intersection_count` | Identification | `int64` | count / text | Extracted static geospatial metric: road intersection count across 100m segment buffer. |
| `road_density_m_per_sqkm` | Identification | `float64` | metres | Extracted static geospatial metric: road density m per sqkm across 100m segment buffer. |
| `road_cut_exposure_proxy` | Identification | `object` | count / text | Extracted static geospatial metric: road cut exposure proxy across 100m segment buffer. |
| `structure_open_road_length_m` | Structure | `float64` | metres | Extracted static geospatial metric: structure open road length m across 100m segment buffer. |
| `structure_tunnel_length_m` | Structure | `float64` | metres | Extracted static geospatial metric: structure tunnel length m across 100m segment buffer. |
| `structure_bridge_length_m` | Structure | `float64` | metres | Extracted static geospatial metric: structure bridge length m across 100m segment buffer. |
| `structure_open_road_fraction` | Structure | `float64` | fraction [0-1] | Extracted static geospatial metric: structure open road fraction across 100m segment buffer. |
| `structure_tunnel_fraction` | Structure | `float64` | fraction [0-1] | Extracted static geospatial metric: structure tunnel fraction across 100m segment buffer. |
| `structure_bridge_fraction` | Structure | `float64` | fraction [0-1] | Extracted static geospatial metric: structure bridge fraction across 100m segment buffer. |
| `structure_dominant_type` | Structure | `str` | metres | Extracted static geospatial metric: structure dominant type across 100m segment buffer. |
| `structure_mixed_flag` | Structure | `bool` | metres | Extracted static geospatial metric: structure mixed flag across 100m segment buffer. |
| `structure_boundary_crossing_flag` | Structure | `bool` | count / text | Extracted static geospatial metric: structure boundary crossing flag across 100m segment buffer. |
| `valid_coverage_pct` | Identification | `float64` | percentage | Extracted static geospatial metric: valid coverage pct across 100m segment buffer. |
| `coverage_quality_flag` | Identification | `str` | count / text | Extracted static geospatial metric: coverage quality flag across 100m segment buffer. |
