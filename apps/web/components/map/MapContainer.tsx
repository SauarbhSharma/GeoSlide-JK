"use client";

import React, { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Layers, MapPin, Compass, Info, AlertTriangle, RotateCcw } from "lucide-react";
import { MapErrorBoundary } from "./MapErrorBoundary";
import { MASTER_LAYER_REGISTRY } from "@/lib/layerRegistry";
import { apiUrl } from "@/lib/api";

interface MapContainerProps {
  onSelectLocation?: (lat: number, lon: number) => void;
  selectedDistrict?: string;
  onSelectDistrict?: (district: string) => void;
  activeLayers?: string[];
}

export interface TerrainInspectionResponse {
  success: boolean;
  code: string;
  message: string;
  location: {
    lat: number;
    lon: number;
  };
  inside_study_area: boolean;
  data_available: boolean;
  district: string;
  terrain?: {
    elevation_m: number | null;
    slope_deg: number | null;
    aspect_deg: number | null;
    hillshade: number | null;
  };
  susceptibility?: {
    probability: number | null;
    class_rating: string | null;
    model: string;
  };
  dynamic_hazard?: {
    rainfall_accum_24h_mm: number | null;
    p90_baseline_mm: number | null;
    hazard_index: number | null;
    hazard_class: string | null;
  };
}

function formatFiniteNumber(val: any, decimals: number = 2, unit: string = ""): string {
  if (val === null || val === undefined) return "N/A";
  const num = Number(val);
  if (!Number.isFinite(num) || num === -9999 || num === -9999.0) return "N/A";
  return `${num.toFixed(decimals)}${unit ? " " + unit : ""}`;
}

export function MapContainer({
  onSelectLocation,
  selectedDistrict,
  onSelectDistrict,
  activeLayers = ["jk_districts", "jk_ut_boundary", "nh44", "susceptibility_prob"],
}: MapContainerProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<any>(null);
  const popupRef = useRef<any>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const [activeTab, setActiveTab] = useState<"layers" | "legend" | "inspect">("layers");
  const [currentDistrict, setCurrentDistrict] = useState<string | null>(selectedDistrict || null);
  const [inspectionData, setInspectionData] = useState<TerrainInspectionResponse | null>(null);
  const [loadingInspect, setLoadingInspect] = useState<boolean>(false);
  const [inspectionError, setInspectionError] = useState<string | null>(null);
  const [basemapError, setBasemapError] = useState<boolean>(false);

  // Synchronized layer visibility state
  const [layersState, setLayersState] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    MASTER_LAYER_REGISTRY.forEach((l) => {
      initial[l.id] = activeLayers.includes(l.id) || l.defaultVisibility;
    });
    return initial;
  });

  // Sync when activeLayers prop changes from parent
  useEffect(() => {
    setLayersState((prev) => {
      const next = { ...prev };
      MASTER_LAYER_REGISTRY.forEach((l) => {
        next[l.id] = activeLayers.includes(l.id);
      });

      if (mapRef.current) {
        const map = mapRef.current;
        MASTER_LAYER_REGISTRY.forEach((l) => {
          if (map.getLayer && map.getLayer(l.id)) {
            map.setLayoutProperty(l.id, "visibility", next[l.id] ? "visible" : "none");
          }
        });
      }
      return next;
    });
  }, [activeLayers]);

  const toggleLayer = (layerId: string) => {
    setLayersState((prev) => {
      const isCurrentlyActive = !!prev[layerId];
      const nextState = !isCurrentlyActive;
      const next = { ...prev, [layerId]: nextState };

      if (mapRef.current) {
        const map = mapRef.current;
        const layerIdMap: Record<string, string[]> = {
          jk_boundary: ["jk-ut-line"],
          district_boundaries: ["jk-districts-fill", "jk-districts-line", "jk-districts-labels"],
          landslide_points: ["jk-landslides-points"],
          landslide_polygons: ["jk-landslides-polygons"],
          faults: ["jk-faults"],
          thrusts: ["jk-thrusts"],
          lineaments: ["jk-lineaments"],
          nh44: ["jk-nh44"],
          major_roads: ["jk-roads"],
          health_facilities: ["jk-health"],
          settlements: ["jk-settlements"],
        };

        const targetIds = layerIdMap[layerId] || [layerId];
        targetIds.forEach((id) => {
          if (map.getLayer && map.getLayer(id)) {
            map.setLayoutProperty(id, "visibility", nextState ? "visible" : "none");
          }
        });
      }
      return next;
    });
  };

  const handleResetView = () => {
    if (mapRef.current) {
      mapRef.current.fitBounds(
        [[73.2, 32.2], [77.8, 35.2]],
        { padding: 40, duration: 1200 }
      );
    }
  };

  useEffect(() => {
    if (!mapContainerRef.current) return;

    const MapClass = maplibregl.Map;
    const PopupClass = maplibregl.Popup;

    const map = new MapClass({
      container: mapContainerRef.current,
      style: {
        version: 8,
        sources: {
          "carto-dark": {
            type: "raster",
            tiles: [
              "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
              "https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
            ],
            tileSize: 256,
            attribution: "&copy; OpenStreetMap contributors &copy; CARTO",
          },
        },
        layers: [
          {
            id: "carto-dark-layer",
            type: "raster",
            source: "carto-dark",
            minzoom: 0,
            maxzoom: 19,
          },
        ],
      },
      center: [75.0, 33.7],
      zoom: 7.2,
      minZoom: 6.5,
      maxZoom: 15.0,
    });

    mapRef.current = map;
    map.fitBounds([[73.2, 32.2], [77.8, 35.2]], { padding: 30 });

    map.on("error", (e: any) => {
      if (e && e.error && (e.error.message?.includes("basemap") || e.error.message?.includes("carto"))) {
        setBasemapError(true);
      }
    });

    setTimeout(() => {
      if (map && map.resize) map.resize();
    }, 200);

    map.on("load", async () => {
      if (map && map.resize) map.resize();

      // Add Raster Tile Layers
      const rasterLayersConfig = [
        { id: "susceptibility_prob", path: "/api/v1/tiles/susceptibility_prob/{z}/{x}/{y}.png", opacity: 0.75 },
        { id: "susceptibility_class", path: "/api/v1/tiles/susceptibility_class/{z}/{x}/{y}.png", opacity: 0.75 },
        { id: "dynamic_hazard_index", path: "/api/v1/tiles/dynamic_hazard_index/{z}/{x}/{y}.png", opacity: 0.75 },
        { id: "dynamic_hazard_class", path: "/api/v1/tiles/dynamic_hazard_class/{z}/{x}/{y}.png", opacity: 0.75 },
        { id: "dem_elevation", path: "/api/v1/tiles/elevation/{z}/{x}/{y}.png", opacity: 0.6 },
        { id: "slope", path: "/api/v1/tiles/slope/{z}/{x}/{y}.png", opacity: 0.6 },
        { id: "aspect", path: "/api/v1/tiles/aspect/{z}/{x}/{y}.png", opacity: 0.5 },
        { id: "hillshade", path: "/api/v1/tiles/hillshade/{z}/{x}/{y}.png", opacity: 0.5 },
      ];

      rasterLayersConfig.forEach((r) => {
        try {
          map.addSource(`${r.id}-src`, {
            type: "raster",
            tiles: [apiUrl(r.path)],
            tileSize: 256,
            minzoom: 0,
            maxzoom: 15,
          });

          const isVisible = activeLayers.includes(r.id) || (r.id === "susceptibility_prob");

          map.addLayer({
            id: r.id,
            type: "raster",
            source: `${r.id}-src`,
            paint: {
              "raster-opacity": r.opacity,
            },
            layout: {
              visibility: isVisible ? "visible" : "none",
            },
          });
        } catch (e) {
          console.warn(`Error adding raster layer ${r.id}:`, e);
        }
      });

      // Add Vector Layers
      try {
        const res = await fetch(apiUrl("/api/v1/districts/boundary"));
        if (res.ok) {
          const districtsGeoJson = await res.json();
          if (districtsGeoJson && districtsGeoJson.type === "FeatureCollection") {
            map.addSource("jk-districts-src", {
              type: "geojson",
              data: districtsGeoJson,
            });

            map.addLayer({
              id: "jk-districts-fill",
              type: "fill",
              source: "jk-districts-src",
              paint: {
                "fill-color": "#0ea5e9",
                "fill-opacity": 0.08,
              },
            });

            map.addLayer({
              id: "jk-districts-line",
              type: "line",
              source: "jk-districts-src",
              paint: {
                "line-color": "#0ea5e9",
                "line-width": 1.2,
                "line-opacity": 0.7,
              },
            });

            map.addLayer({
              id: "jk-ut-line",
              type: "line",
              source: "jk-districts-src",
              paint: {
                "line-color": "#38bdf8",
                "line-width": 2.5,
                "line-opacity": 0.95,
              },
            });

            map.addLayer({
              id: "jk-districts-labels",
              type: "symbol",
              source: "jk-districts-src",
              layout: {
                "text-field": ["get", "display_name"],
                "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
                "text-size": 11,
                "text-transform": "uppercase",
                "text-allow-overlap": false,
              },
              paint: {
                "text-color": "#e2e8f0",
                "text-halo-color": "#090d16",
                "text-halo-width": 2,
              },
            });
          }
        }
      } catch (err) {
        console.warn("Could not fetch districts boundary:", err);
      }

      const loadVectorLayer = async (
        layerId: string,
        backendId: string,
        type: "circle" | "line" | "fill",
        paintProps: any
      ) => {
        try {
          const res = await fetch(apiUrl(`/api/v1/static-layers/${backendId}`));
          if (res.ok) {
            const data = await res.json();
            if (data && data.type === "FeatureCollection") {
              map.addSource(`${layerId}-src`, { type: "geojson", data });
              map.addLayer({
                id: layerId,
                type: type as any,
                source: `${layerId}-src`,
                paint: paintProps,
              });
            }
          }
        } catch (e) {
          console.warn(`Layer ${layerId} fetch failed:`, e);
        }
      };

      await loadVectorLayer("jk-landslides-points", "landslides_points", "circle", {
        "circle-radius": 4,
        "circle-color": "#ef4444",
        "circle-stroke-width": 1,
        "circle-stroke-color": "#7f1d1d",
        "circle-opacity": 0.85,
      });

      await loadVectorLayer("jk-landslides-polygons", "landslides_polygons", "fill", {
        "fill-color": "#dc2626",
        "fill-opacity": 0.45,
        "fill-outline-color": "#991b1b",
      });

      await loadVectorLayer("jk-faults", "faults", "line", {
        "line-color": "#ec4899",
        "line-width": 2.2,
        "line-dasharray": [2, 1],
      });

      await loadVectorLayer("jk-thrusts", "thrusts", "line", {
        "line-color": "#a855f7",
        "line-width": 2.5,
      });

      await loadVectorLayer("jk-lineaments", "lineaments", "line", {
        "line-color": "#c084fc",
        "line-width": 1.5,
      });

      await loadVectorLayer("jk-nh44", "nh44", "line", {
        "line-color": "#eab308",
        "line-width": 3.5,
      });

      await loadVectorLayer("jk-roads", "major_roads", "line", {
        "line-color": "#f59e0b",
        "line-width": 1.5,
        "line-opacity": 0.7,
      });

      await loadVectorLayer("jk-settlements", "settlements", "circle", {
        "circle-radius": 3,
        "circle-color": "#38bdf8",
        "circle-opacity": 0.6,
      });

      await loadVectorLayer("jk-health", "health_facilities", "circle", {
        "circle-radius": 3.5,
        "circle-color": "#10b981",
        "circle-stroke-width": 1,
        "circle-stroke-color": "#064e3b",
      });
    });

    // Map Click Inspector Handler
    map.on("click", async (e: any) => {
      if (!e || !e.lngLat) return;
      const { lat, lng } = e.lngLat;

      if (!Number.isFinite(lat) || !Number.isFinite(lng) || lat < -90 || lat > 90 || lng < -180 || lng > 180) {
        setInspectionError("Invalid coordinates clicked.");
        return;
      }

      if (onSelectLocation) {
        try {
          onSelectLocation(lat, lng);
        } catch (err) {
          console.warn("Error in onSelectLocation callback:", err);
        }
      }

      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      const controller = new AbortController();
      abortControllerRef.current = controller;

      setLoadingInspect(true);
      setInspectionError(null);
      setActiveTab("inspect");

      try {
        const url = apiUrl(`/api/v1/terrain/value?lat=${lat.toFixed(5)}&lon=${lng.toFixed(5)}`);
        const res = await fetch(url, { signal: controller.signal });

        if (!res.ok) {
          let errDetail = `HTTP ${res.status}`;
          try {
            const errJson = await res.json();
            if (errJson && errJson.detail) errDetail = errJson.detail;
          } catch (_) {}

          setInspectionData({
            success: false,
            code: "API_ERROR",
            message: errDetail,
            location: { lat, lon: lng },
            inside_study_area: false,
            data_available: false,
            district: "Outside J&K UT Boundary"
          });
          setInspectionError(errDetail);
          return;
        }

        const data: TerrainInspectionResponse = await res.json();
        if (controller.signal.aborted) return;

        setInspectionData(data);
        if (data.district && data.district !== "Outside J&K UT Boundary") {
          setCurrentDistrict(data.district);
          if (onSelectDistrict) onSelectDistrict(data.district);
        }

        if (popupRef.current) popupRef.current.remove();

        const safeDist = data.district || "Jammu and Kashmir";
        const safeElev = formatFiniteNumber(data.terrain?.elevation_m, 2, "m ASL");
        const safeSlope = formatFiniteNumber(data.terrain?.slope_deg, 2, "°");
        const safeAspect = formatFiniteNumber(data.terrain?.aspect_deg, 2, "°");

        const safeSuscProb = data.susceptibility?.probability != null ? (data.susceptibility.probability * 100).toFixed(1) + '%' : 'N/A';
        const safeSuscClass = data.susceptibility?.class_rating || 'N/A';
        const safeHazIdx = data.dynamic_hazard?.hazard_index != null ? data.dynamic_hazard.hazard_index.toFixed(4) : 'N/A';
        const safeHazClass = data.dynamic_hazard?.hazard_class || 'N/A';
        const safeRain = data.dynamic_hazard?.rainfall_accum_24h_mm != null ? data.dynamic_hazard.rainfall_accum_24h_mm.toFixed(1) + ' mm' : 'N/A';

        const popupHtml = `
          <div style="font-family: sans-serif; padding: 10px; color: #f8fafc; background: #090d16; border: 1px solid #334155; border-radius: 8px; font-size: 12px; line-height: 1.5; min-width: 240px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
            <div style="font-weight: bold; color: #38bdf8; font-size: 13px; margin-bottom: 6px; border-bottom: 1px solid #1e293b; padding-bottom: 4px; display: flex; justify-content: space-between; align-items: center;">
              <span>${safeDist}</span>
              <span style="font-size: 9px; font-family: monospace; background: #0284c7; color: #ffffff; padding: 2px 6px; border-radius: 4px;">v1.0.0</span>
            </div>
            <div style="color: #cbd5e1;"><b>Lat / Lon:</b> ${formatFiniteNumber(lat, 4)}°N, ${formatFiniteNumber(lng, 4)}°E</div>
            <div style="margin-top: 6px; background: #0f172a; padding: 6px; border-radius: 4px; border: 1px solid #1e293b;">
              <div><b>Elevation:</b> <span style="color: #facc15; font-weight: bold;">${safeElev}</span></div>
              <div><b>Slope Angle:</b> <span style="color: #f97316; font-weight: bold;">${safeSlope}</span></div>
              <div><b>Aspect:</b> <span style="color: #c084fc;">${safeAspect}</span></div>
            </div>
            <div style="margin-top: 6px; background: #0f172a; padding: 6px; border-radius: 4px; border: 1px solid #1e293b;">
              <div><b>Susceptibility:</b> <span style="color: #f59e0b; font-weight: bold;">${safeSuscClass} (${safeSuscProb})</span></div>
              <div><b>Dynamic Hazard:</b> <span style="color: #ef4444; font-weight: bold;">${safeHazClass} (${safeHazIdx})</span></div>
              <div><b>24h Rain Proxy:</b> <span style="color: #38bdf8;">${safeRain}</span></div>
            </div>
            <div style="font-size: 9px; color: #94a3b8; margin-top: 6px; border-top: 1px solid #1e293b; padding-top: 4px;">
              <div>Web Map: EPSG:4326 / Web Mercator</div>
              <div>Processing CRS: EPSG:32643</div>
              <div style="color: #64748b; margin-top: 2px;">${data.data_available ? 'Copernicus GLO-30 & XGBoost 100m Grid' : data.message || 'No terrain data'}</div>
            </div>
          </div>
        `;

        if (PopupClass) {
          popupRef.current = new PopupClass({ closeButton: true, className: "custom-popup" })
            .setLngLat([lng, lat])
            .setHTML(popupHtml)
            .addTo(map);
        }

      } catch (err: any) {
        if (err.name === "AbortError") return;
        console.error("Terrain inspection request error:", err);
        setInspectionError("Unable to fetch location data. Backend server may be offline.");
        setInspectionData({
          success: false,
          code: "NETWORK_ERROR",
          message: "Unable to connect to backend server.",
          location: { lat, lon: lng },
          inside_study_area: false,
          data_available: false,
          district: "Unknown"
        });
      } finally {
        setLoadingInspect(false);
      }
    });

    return () => {
      if (abortControllerRef.current) abortControllerRef.current.abort();
      if (mapRef.current) mapRef.current.remove();
    };
  }, [onSelectLocation, onSelectDistrict]);

  return (
    <div className="relative w-full h-full min-h-[620px] bg-navy-950 rounded-xl overflow-hidden border border-slate-800 shadow-2xl flex">
      {/* Map Container Canvas */}
      <div ref={mapContainerRef} className="w-full h-full min-h-[620px]" />

      {/* Basemap Fallback Alert Banner */}
      {basemapError && (
        <div className="absolute top-16 left-4 z-20 bg-amber-950/90 border border-amber-500/80 text-amber-200 px-3 py-1.5 rounded-lg text-xs flex items-center space-x-2 shadow-xl">
          <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
          <span>Basemap unavailable — analytical layers & local boundaries remain fully operational.</span>
        </div>
      )}

      {/* Title, CRS Wording & Reset Button Banner */}
      <div className="absolute top-4 left-4 z-10 bg-slate-900/95 backdrop-blur-md p-3 rounded-lg border border-slate-700/80 shadow-xl max-w-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
            <h2 className="text-xs font-bold text-slate-100 uppercase tracking-wide">
              FULL J&K UT GEOGRAPHIC MAP
            </h2>
          </div>
          <button
            onClick={handleResetView}
            className="flex items-center space-x-1 bg-sky-950 hover:bg-sky-900 border border-sky-600/50 text-sky-300 text-[10px] px-2 py-0.5 rounded transition-colors font-mono"
            title="Reset Map to J&K Boundary"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Reset to J&K</span>
          </button>
        </div>
        <p className="text-xs text-sky-400 font-medium mt-1">
          Copernicus DEM & 20-District Boundaries
        </p>
        <div className="text-[10px] text-slate-400 font-mono mt-1 space-y-0.5 border-t border-slate-800 pt-1">
          <div>Web Map: <span className="text-slate-200">EPSG:4326 / Web Mercator</span></div>
          <div>Terrain Processing CRS: <span className="text-slate-200">EPSG:32643</span></div>
        </div>
      </div>

      {/* Floating Control Panel */}
      <div className="absolute top-4 right-4 z-10 w-80 bg-slate-900/95 backdrop-blur-md rounded-xl border border-slate-700/80 shadow-2xl overflow-hidden flex flex-col text-slate-200">
        {/* Tab Headers */}
        <div className="flex border-b border-slate-800 bg-slate-950/80">
          <button
            onClick={() => setActiveTab("layers")}
            className={`flex-1 py-2.5 text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors ${
              activeTab === "layers"
                ? "text-sky-400 border-b-2 border-sky-400 bg-slate-900/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Map Layers</span>
          </button>
          <button
            onClick={() => setActiveTab("inspect")}
            className={`flex-1 py-2.5 text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors ${
              activeTab === "inspect"
                ? "text-sky-400 border-b-2 border-sky-400 bg-slate-900/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Compass className="w-3.5 h-3.5" />
            <span>Inspector</span>
          </button>
          <button
            onClick={() => setActiveTab("legend")}
            className={`flex-1 py-2.5 text-xs font-semibold flex items-center justify-center space-x-1.5 transition-colors ${
              activeTab === "legend"
                ? "text-sky-400 border-b-2 border-sky-400 bg-slate-900/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Info className="w-3.5 h-3.5" />
            <span>Legend</span>
          </button>
        </div>

        {/* Tab Content */}
        <div className="p-3.5 max-h-[460px] overflow-y-auto space-y-3 text-xs">
          {activeTab === "layers" && (
            <MapErrorBoundary fallbackMessage="Unable to display layer controls.">
              <div className="space-y-3">
                <div className="text-[11px] font-bold uppercase text-slate-400 tracking-wider">
                  Master Layer Registry
                </div>

                <div className="space-y-1.5">
                  {MASTER_LAYER_REGISTRY.map((layer) => {
                    const isChecked = layersState[layer.id] ?? layer.defaultVisibility;
                    const isAvailable = layer.availability === "Available" || layer.availability === "Scenario / Proxy Mode";
                    return (
                      <label
                        key={layer.id}
                        className={`flex items-center justify-between cursor-pointer p-2 rounded border text-xs transition-colors ${
                          isAvailable
                            ? "hover:bg-slate-800/60 border-slate-800 bg-slate-950/40"
                            : "opacity-60 border-slate-800/50 bg-slate-950/20 cursor-not-allowed"
                        }`}
                      >
                        <div className="flex flex-col pr-2">
                          <span className="font-semibold text-slate-200">{layer.displayName}</span>
                          <span className="text-[9.5px] text-slate-400 font-mono">
                            {layer.availability} • {layer.source}
                          </span>
                        </div>
                        <input
                          type="checkbox"
                          disabled={!isAvailable}
                          checked={isChecked && isAvailable}
                          onChange={() => toggleLayer(layer.id)}
                          className="rounded bg-slate-800 border-slate-700 text-sky-500 focus:ring-0 shrink-0"
                        />
                      </label>
                    );
                  })}
                </div>
              </div>
            </MapErrorBoundary>
          )}

          {activeTab === "inspect" && (
            <MapErrorBoundary fallbackMessage="Unable to display inspector details. The map remains fully operational.">
              <div className="space-y-3">
                <div className="text-[11px] font-bold uppercase text-slate-400 tracking-wider">
                  Terrain Cell Inspector
                </div>

                {loadingInspect ? (
                  <div className="py-6 text-center text-slate-400 animate-pulse">
                    Sampling terrain & ML rasters at clicked location...
                  </div>
                ) : inspectionError ? (
                  <div className="space-y-2 bg-rose-950/40 p-3 rounded-lg border border-rose-800/60 text-rose-200">
                    <div className="flex items-center space-x-1.5 font-bold text-rose-400">
                      <AlertTriangle className="w-4 h-4 shrink-0" />
                      <span>Notice</span>
                    </div>
                    <p className="text-xs">{inspectionError}</p>
                    <p className="text-[10px] text-slate-400">The map remains fully operational for further inspection.</p>
                  </div>
                ) : inspectionData ? (
                  <div className="space-y-2 bg-slate-950/80 p-3 rounded-lg border border-slate-800">
                    <div className="text-sm font-bold text-sky-400 border-b border-slate-800 pb-1.5 flex items-center justify-between">
                      <span>{inspectionData.district || "Jammu and Kashmir"}</span>
                      {inspectionData.data_available ? (
                        <span className="text-[10px] font-mono bg-emerald-950 text-emerald-300 px-1.5 py-0.5 rounded border border-emerald-700/60">
                          Data Available
                        </span>
                      ) : (
                        <span className="text-[10px] font-mono bg-amber-950 text-amber-300 px-1.5 py-0.5 rounded border border-amber-700/60">
                          {inspectionData.code || "No Data"}
                        </span>
                      )}
                    </div>

                    {!inspectionData.data_available && (
                      <div className="bg-amber-950/30 border border-amber-800/50 p-2 rounded text-amber-200 text-xs mt-1">
                        {inspectionData.message || "No valid terrain data at this location."}
                      </div>
                    )}

                    <div className="grid grid-cols-2 gap-2 text-xs pt-1">
                      <div>
                        <span className="text-slate-400 block text-[10px]">Elevation</span>
                        <span className="font-semibold text-amber-400 text-sm">
                          {formatFiniteNumber(inspectionData.terrain?.elevation_m, 2, "m")}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px]">Slope Angle</span>
                        <span className="font-semibold text-orange-400 text-sm">
                          {formatFiniteNumber(inspectionData.terrain?.slope_deg, 2, "°")}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px]">Aspect</span>
                        <span className="font-semibold text-slate-200">
                          {formatFiniteNumber(inspectionData.terrain?.aspect_deg, 2, "°")}
                        </span>
                      </div>
                      <div>
                        <span className="text-slate-400 block text-[10px]">Lat / Lon</span>
                        <span className="font-mono text-[11px] text-slate-300">
                          {formatFiniteNumber(inspectionData.location?.lat, 3)}°, {formatFiniteNumber(inspectionData.location?.lon, 3)}°
                        </span>
                      </div>
                    </div>

                    {inspectionData.susceptibility && (
                      <div className="grid grid-cols-2 gap-2 text-xs pt-2 border-t border-slate-800/80">
                        <div>
                          <span className="text-slate-400 block text-[10px]">Susceptibility</span>
                          <span className="font-bold text-amber-400 text-sm">
                            {inspectionData.susceptibility.class_rating || "N/A"}
                          </span>
                        </div>
                        <div>
                          <span className="text-slate-400 block text-[10px]">Probability</span>
                          <span className="font-bold text-amber-300 text-sm">
                            {inspectionData.susceptibility.probability != null
                              ? (inspectionData.susceptibility.probability * 100).toFixed(1) + "%"
                              : "N/A"}
                          </span>
                        </div>
                        <div>
                          <span className="text-slate-400 block text-[10px]">Dynamic Hazard</span>
                          <span className="font-bold text-rose-400 text-sm">
                            {inspectionData.dynamic_hazard?.hazard_class || "N/A"}
                          </span>
                        </div>
                        <div>
                          <span className="text-slate-400 block text-[10px]">24h Rain Proxy</span>
                          <span className="font-bold text-sky-400 text-sm">
                            {inspectionData.dynamic_hazard?.rainfall_accum_24h_mm != null
                              ? inspectionData.dynamic_hazard.rainfall_accum_24h_mm.toFixed(1) + " mm"
                              : "N/A"}
                          </span>
                        </div>
                      </div>
                    )}

                    <div className="text-[10px] text-slate-500 pt-2 border-t border-slate-800/80 space-y-0.5 font-mono">
                      <div>Web Map: EPSG:4326 / Web Mercator</div>
                      <div>Processing CRS: EPSG:32643</div>
                      <div className="text-slate-400">Copernicus GLO-30 & XGBoost 100m Grid</div>
                    </div>
                  </div>
                ) : (
                  <div className="py-6 text-center text-slate-400">
                    <MapPin className="w-8 h-8 text-sky-500/50 mx-auto mb-2" />
                    Click any point on the map to inspect terrain elevation, slope, ML susceptibility & dynamic hazard.
                  </div>
                )}
              </div>
            </MapErrorBoundary>
          )}

          {activeTab === "legend" && (
            <MapErrorBoundary fallbackMessage="Unable to display legend details.">
              <div className="space-y-3">
                <div className="text-[11px] font-bold uppercase text-slate-400 tracking-wider">
                  Geospatial Symbology Legend
                </div>
                <div className="space-y-2 text-xs">
                  <div className="flex items-center space-x-2.5">
                    <span className="w-3.5 h-3.5 border-2 border-sky-400 bg-sky-500/10 rounded" />
                    <span>20 J&K UT Districts</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <span className="w-3 h-3 rounded-full bg-red-500 border border-red-900" />
                    <span>NGDR Landslide Points (2,370)</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <span className="w-3.5 h-2.5 bg-red-600/50 border border-red-800 rounded-sm" />
                    <span>NGDR Landslide Polygons (7,436)</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <span className="w-4 h-1 bg-pink-500 rounded" />
                    <span>Tectonic Fault Lines (GSI NGDR)</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <span className="w-4 h-1 bg-purple-500 rounded" />
                    <span>Thrust Fault Lines (GSI NGDR)</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <span className="w-4 h-1 bg-purple-400 rounded" />
                    <span>Structural Lineaments (774)</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <span className="w-4 h-1.5 bg-amber-400 rounded" />
                    <span>NH-44 Highway Corridor</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <span className="w-4 h-1 bg-amber-500 rounded" />
                    <span>Statewide Major Roads (4,762)</span>
                  </div>
                  <div className="flex items-center space-x-2.5">
                    <span className="w-3 h-3 rounded-full bg-emerald-400 border border-emerald-800" />
                    <span>Hospitals & Healthcare (877)</span>
                  </div>
                </div>
              </div>
            </MapErrorBoundary>
          )}
        </div>
      </div>
    </div>
  );
}
