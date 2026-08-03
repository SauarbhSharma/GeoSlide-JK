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

  // Stable callback refs to prevent map recreation when props change
  const onSelectLocationRef = useRef(onSelectLocation);
  useEffect(() => {
    onSelectLocationRef.current = onSelectLocation;
  }, [onSelectLocation]);

  const onSelectDistrictRef = useRef(onSelectDistrict);
  useEffect(() => {
    onSelectDistrictRef.current = onSelectDistrict;
  }, [onSelectDistrict]);

  const [activeTab, setActiveTab] = useState<"layers" | "legend" | "inspect">("layers");
  const [currentDistrict, setCurrentDistrict] = useState<string | null>(selectedDistrict || null);
  const [inspectionData, setInspectionData] = useState<TerrainInspectionResponse | null>(null);
  const [loadingInspect, setLoadingInspect] = useState<boolean>(false);
  const [inspectionError, setInspectionError] = useState<string | null>(null);
  const [basemapError, setBasemapError] = useState<boolean>(false);
  const [isDrawerCollapsed, setIsDrawerCollapsed] = useState<boolean>(false);

  // Global unhandled promise rejection handler to safely prevent Next.js error overlays for expected MapLibre tile AbortError
  useEffect(() => {
    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      const reason = event.reason;
      if (
        reason &&
        (reason.name === "AbortError" ||
          (typeof reason.message === "string" &&
            (reason.message.includes("signal is aborted") ||
              reason.message.includes("aborted without reason") ||
              reason.message.includes("AbortError") ||
              reason.message.includes("user aborted"))))
      ) {
        event.preventDefault();
      }
    };

    window.addEventListener("unhandledrejection", handleUnhandledRejection);
    return () => {
      window.removeEventListener("unhandledrejection", handleUnhandledRejection);
    };
  }, []);

  // Synchronized layer visibility state
  const [layersState, setLayersState] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {};
    MASTER_LAYER_REGISTRY.forEach((l) => {
      initial[l.id] = activeLayers.includes(l.id) || l.defaultVisibility;
    });
    return initial;
  });

  // Helper mapping for frontend layer IDs to MapLibre layer IDs
  const getMapLayerIds = (layerId: string): string[] => {
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
    return layerIdMap[layerId] || [layerId];
  };

  // Sync layer visibility whenever activeLayers prop changes without destroying map
  useEffect(() => {
    setLayersState((prev) => {
      const next = { ...prev };
      MASTER_LAYER_REGISTRY.forEach((l) => {
        next[l.id] = activeLayers.includes(l.id);
      });

      if (mapRef.current) {
        const map = mapRef.current;
        MASTER_LAYER_REGISTRY.forEach((l) => {
          const isVisible = next[l.id];
          const targetIds = getMapLayerIds(l.id);
          targetIds.forEach((id) => {
            if (map.getLayer && map.getLayer(id)) {
              map.setLayoutProperty(id, "visibility", isVisible ? "visible" : "none");
            }
          });
        });
      }
      return next;
    });
  }, [activeLayers]);

  // Sync selected district prop changes
  useEffect(() => {
    if (selectedDistrict) {
      setCurrentDistrict(selectedDistrict);
    }
  }, [selectedDistrict]);

  const toggleLayer = (layerId: string) => {
    setLayersState((prev) => {
      const isCurrentlyActive = !!prev[layerId];
      const nextState = !isCurrentlyActive;
      const next = { ...prev, [layerId]: nextState };

      if (mapRef.current) {
        const map = mapRef.current;
        const targetIds = getMapLayerIds(layerId);
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

  // Single MapLibre Initialization Effect
  useEffect(() => {
    if (!mapContainerRef.current) return;
    if (mapRef.current) return; // Prevent double initialization in React StrictMode

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
      const isAbortError =
        e?.error?.name === "AbortError" ||
        (typeof e?.error?.message === "string" &&
          (e.error.message.includes("signal is aborted") ||
            e.error.message.includes("aborted without reason") ||
            e.error.message.includes("AbortError"))) ||
        (typeof e?.message === "string" && e.message.includes("aborted"));

      if (isAbortError) return; // Safely ignore tile cancellation

      if (e && e.error && (e.error.message?.includes("basemap") || e.error.message?.includes("carto"))) {
        setBasemapError(true);
      }
    });

    setTimeout(() => {
      if (mapRef.current && mapRef.current.resize) {
        mapRef.current.resize();
      }
    }, 200);

    map.on("load", async () => {
      if (!mapRef.current) return;
      if (map.resize) map.resize();

      // Add Raster Tile Layers safely
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
          if (!map.getSource(`${r.id}-src`)) {
            map.addSource(`${r.id}-src`, {
              type: "raster",
              tiles: [apiUrl(r.path)],
              tileSize: 256,
              minzoom: 0,
              maxzoom: 15,
            });
          }

          if (!map.getLayer(r.id)) {
            const isVisible = activeLayers.includes(r.id) || r.id === "susceptibility_prob";
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
          }
        } catch (e) {
          console.warn(`Error adding raster layer ${r.id}:`, e);
        }
      });

      // Add Vector Layers safely
      try {
        const res = await fetch(apiUrl("/api/v1/districts/boundary"));
        if (res.ok) {
          const districtsGeoJson = await res.json();
          if (districtsGeoJson && districtsGeoJson.type === "FeatureCollection") {
            if (!map.getSource("jk-districts-src")) {
              map.addSource("jk-districts-src", {
                type: "geojson",
                data: districtsGeoJson,
              });
            }

            if (!map.getLayer("jk-districts-fill")) {
              map.addLayer({
                id: "jk-districts-fill",
                type: "fill",
                source: "jk-districts-src",
                paint: {
                  "fill-color": "#0ea5e9",
                  "fill-opacity": 0.08,
                },
              });
            }

            if (!map.getLayer("jk-districts-line")) {
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
            }

            if (!map.getLayer("jk-ut-line")) {
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
            }

            if (!map.getLayer("jk-districts-labels")) {
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
              if (!map.getSource(`${layerId}-src`)) {
                map.addSource(`${layerId}-src`, { type: "geojson", data });
              }
              if (!map.getLayer(layerId)) {
                map.addLayer({
                  id: layerId,
                  type: type as any,
                  source: `${layerId}-src`,
                  paint: paintProps,
                });
              }
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

    // Map Click Inspector Handler (updates React state safely without recreating map)
    map.on("click", async (e: any) => {
      if (!e || !e.lngLat) return;
      const { lat, lng } = e.lngLat;

      if (!Number.isFinite(lat) || !Number.isFinite(lng) || lat < -90 || lat > 90 || lng < -180 || lng > 180) {
        setInspectionError("Invalid coordinates clicked.");
        return;
      }

      if (onSelectLocationRef.current) {
        try {
          onSelectLocationRef.current(lat, lng);
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
            district: "Outside J&K UT Boundary",
          });
          setInspectionError(errDetail);
          return;
        }

        const data: TerrainInspectionResponse = await res.json();
        if (controller.signal.aborted) return;

        setInspectionData(data);
        if (data.district && data.district !== "Outside J&K UT Boundary") {
          setCurrentDistrict(data.district);
          if (onSelectDistrictRef.current) onSelectDistrictRef.current(data.district);
        }

        if (popupRef.current) {
          try {
            popupRef.current.remove();
          } catch (_) {}
          popupRef.current = null;
        }

        const safeDist = data.district || "Jammu and Kashmir";
        const safeElev = formatFiniteNumber(data.terrain?.elevation_m, 2, "m ASL");
        const safeSlope = formatFiniteNumber(data.terrain?.slope_deg, 2, "°");
        const safeAspect = formatFiniteNumber(data.terrain?.aspect_deg, 2, "°");
        const safeSuscProb = data.susceptibility?.probability != null ? (data.susceptibility.probability * 100).toFixed(1) + "%" : "N/A";
        const safeSuscClass = data.susceptibility?.class_rating || "N/A";
        const safeHazIdx = data.dynamic_hazard?.hazard_index != null ? data.dynamic_hazard.hazard_index.toFixed(4) : "N/A";
        const safeHazClass = data.dynamic_hazard?.hazard_class || "N/A";
        const safeRain = data.dynamic_hazard?.rainfall_accum_24h_mm != null ? data.dynamic_hazard.rainfall_accum_24h_mm.toFixed(1) + " mm" : "N/A";

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
              <div style="color: #64748b; margin-top: 2px;">${data.data_available ? "Copernicus GLO-30 & XGBoost 100m Grid" : data.message || "No terrain data"}</div>
            </div>
          </div>
        `;

        if (PopupClass && mapRef.current) {
          popupRef.current = new PopupClass({ closeButton: true, className: "custom-popup" })
            .setLngLat([lng, lat])
            .setHTML(popupHtml)
            .addTo(mapRef.current);
        }
      } catch (err: any) {
        if (err.name === "AbortError" || err.message?.includes("aborted")) return;
        console.error("Terrain inspection request error:", err);
        setInspectionError("Unable to fetch location data. Backend server may be offline.");
        setInspectionData({
          success: false,
          code: "NETWORK_ERROR",
          message: "Unable to connect to backend server.",
          location: { lat, lon: lng },
          inside_study_area: false,
          data_available: false,
          district: "Unknown",
        });
      } finally {
        setLoadingInspect(false);
      }
    });

    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
        abortControllerRef.current = null;
      }
      if (popupRef.current) {
        try {
          popupRef.current.remove();
        } catch (_) {}
        popupRef.current = null;
      }
      if (mapRef.current) {
        try {
          mapRef.current.remove();
        } catch (_) {}
        mapRef.current = null;
      }
    };
  }, []); // Run map initialization ONCE on mount

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
      <MapErrorBoundary>
        {isDrawerCollapsed ? (
          <button
            onClick={() => setIsDrawerCollapsed(false)}
            className="absolute top-4 right-4 z-10 bg-slate-900/95 hover:bg-slate-800 backdrop-blur-md px-3 py-2 rounded-xl border border-slate-700 text-sky-400 text-xs font-semibold flex items-center space-x-2 shadow-2xl transition-all"
            title="Expand Map Layers Drawer"
          >
            <Layers className="w-4 h-4" />
            <span>Map Layers & Inspector</span>
          </button>
        ) : (
          <div className="absolute top-4 right-4 z-10 w-80 bg-slate-900/95 backdrop-blur-md rounded-xl border border-slate-700/80 shadow-2xl overflow-hidden flex flex-col text-slate-200">
            {/* Tab Headers */}
            <div className="flex items-center justify-between border-b border-slate-800 bg-slate-950/80 pr-2">
              <div className="flex flex-1">
                <button
                  onClick={() => setActiveTab("layers")}
                  className={`flex-1 py-2.5 text-xs font-semibold flex items-center justify-center space-x-1 transition-colors ${
                    activeTab === "layers"
                      ? "bg-sky-950/90 text-sky-400 border-b-2 border-sky-500"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50"
                  }`}
                >
                  <Layers className="w-3.5 h-3.5" />
                  <span>Layers</span>
                </button>
                <button
                  onClick={() => setActiveTab("legend")}
                  className={`flex-1 py-2.5 text-xs font-semibold flex items-center justify-center space-x-1 transition-colors ${
                    activeTab === "legend"
                      ? "bg-sky-950/90 text-sky-400 border-b-2 border-sky-500"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50"
                  }`}
                >
                  <Info className="w-3.5 h-3.5" />
                  <span>Legend</span>
                </button>
                <button
                  onClick={() => setActiveTab("inspect")}
                  className={`flex-1 py-2.5 text-xs font-semibold flex items-center justify-center space-x-1 transition-colors ${
                    activeTab === "inspect"
                      ? "bg-sky-950/90 text-sky-400 border-b-2 border-sky-500"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50"
                  }`}
                >
                  <Compass className="w-3.5 h-3.5" />
                  <span>Inspect</span>
                </button>
              </div>
              <button
                onClick={() => setIsDrawerCollapsed(true)}
                className="p-1 text-slate-400 hover:text-white rounded hover:bg-slate-800 transition-colors"
                title="Collapse Drawer"
              >
                ✕
              </button>
            </div>

        {/* Tab Body */}
        <div className="p-4 max-h-[500px] overflow-y-auto space-y-4 font-sans">
          {/* TAB 1: LAYERS */}
          {activeTab === "layers" && (
            <div className="space-y-3">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">
                Data Layer Visibility
              </div>

              {MASTER_LAYER_REGISTRY.map((layer) => {
                const isActive = !!layersState[layer.id];
                return (
                  <label
                    key={layer.id}
                    className={`flex items-center justify-between p-2.5 rounded-lg border transition-all cursor-pointer ${
                      isActive
                        ? "bg-slate-800/80 border-sky-600/50 text-slate-100 shadow"
                        : "bg-slate-950/40 border-slate-800 text-slate-400 hover:bg-slate-900"
                    }`}
                  >
                    <div className="flex items-center space-x-3 pr-2">
                      <input
                        type="checkbox"
                        checked={isActive}
                        onChange={() => toggleLayer(layer.id)}
                        className="rounded border-slate-700 bg-slate-900 text-sky-500 focus:ring-sky-500 w-4 h-4"
                      />
                      <div>
                        <div className="text-xs font-medium leading-snug">{layer.displayName}</div>
                        <div className="text-[10px] text-slate-500 leading-tight mt-0.5">
                          {layer.units} • {layer.category}
                        </div>
                      </div>
                    </div>
                    <span
                      className="w-3 h-3 rounded-full shrink-0 border border-slate-700"
                      style={{ backgroundColor: layer.legend?.color || "#0ea5e9" }}
                    />
                  </label>
                );
              })}
            </div>
          )}

          {/* TAB 2: LEGEND */}
          {activeTab === "legend" && (
            <div className="space-y-4">
              <div>
                <h3 className="text-xs font-bold uppercase text-slate-400 mb-2">
                  Susceptibility Probability Rating
                </h3>
                <div className="space-y-1.5 text-xs">
                  <div className="flex items-center justify-between p-1.5 rounded bg-emerald-950/40 border border-emerald-800/30">
                    <span className="flex items-center space-x-2">
                      <span className="w-3 h-3 rounded bg-emerald-500 inline-block" />
                      <span>Very Low (0.00 – 0.15)</span>
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">Class 1</span>
                  </div>
                  <div className="flex items-center justify-between p-1.5 rounded bg-green-950/40 border border-green-800/30">
                    <span className="flex items-center space-x-2">
                      <span className="w-3 h-3 rounded bg-green-400 inline-block" />
                      <span>Low (0.15 – 0.35)</span>
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">Class 2</span>
                  </div>
                  <div className="flex items-center justify-between p-1.5 rounded bg-amber-950/40 border border-amber-800/30">
                    <span className="flex items-center space-x-2">
                      <span className="w-3 h-3 rounded bg-amber-400 inline-block" />
                      <span>Moderate (0.35 – 0.55)</span>
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">Class 3</span>
                  </div>
                  <div className="flex items-center justify-between p-1.5 rounded bg-orange-950/40 border border-orange-800/30">
                    <span className="flex items-center space-x-2">
                      <span className="w-3 h-3 rounded bg-orange-500 inline-block" />
                      <span>High (0.55 – 0.75)</span>
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">Class 4</span>
                  </div>
                  <div className="flex items-center justify-between p-1.5 rounded bg-rose-950/40 border border-rose-800/30">
                    <span className="flex items-center space-x-2">
                      <span className="w-3 h-3 rounded bg-rose-600 inline-block" />
                      <span>Very High (0.75 – 1.00)</span>
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">Class 5</span>
                  </div>
                </div>
              </div>

              <div className="border-t border-slate-800 pt-3">
                <h3 className="text-xs font-bold uppercase text-slate-400 mb-2">
                  Dynamic Hazard Index Rating
                </h3>
                <div className="space-y-1 text-xs text-slate-300">
                  <div className="flex justify-between">
                    <span>Low Hazard:</span>
                    <span className="font-mono text-emerald-400">&lt; 0.25</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Moderate Hazard:</span>
                    <span className="font-mono text-amber-400">0.25 – 0.50</span>
                  </div>
                  <div className="flex justify-between">
                    <span>High Hazard:</span>
                    <span className="font-mono text-orange-400">0.50 – 0.75</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Extreme Hazard:</span>
                    <span className="font-mono text-rose-500">&gt; 0.75</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: INSPECTOR */}
          {activeTab === "inspect" && (
            <div className="space-y-3">
              <div className="text-xs text-slate-400 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800 flex items-start space-x-2">
                <MapPin className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
                <div>
                  <div className="font-semibold text-slate-200">Point Inspector Active</div>
                  <div className="text-[11px] mt-0.5 text-slate-400">
                    Click anywhere on the map to sample underlying 100m grid cell values.
                  </div>
                </div>
              </div>

              {loadingInspect && (
                <div className="p-4 text-center text-xs text-sky-400 bg-sky-950/30 rounded-lg border border-sky-800/40 animate-pulse">
                  Sampling terrain & hazard data...
                </div>
              )}

              {inspectionError && !loadingInspect && (
                <div className="p-3 text-xs text-rose-300 bg-rose-950/40 rounded-lg border border-rose-800/50">
                  {inspectionError}
                </div>
              )}

              {inspectionData && !loadingInspect && (
                <div className="space-y-3 text-xs">
                  {/* District & Location */}
                  <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800 space-y-1">
                    <div className="text-slate-400 text-[10px] uppercase font-mono tracking-wider">
                      Selected Location
                    </div>
                    <div className="text-sm font-bold text-sky-400">{inspectionData.district}</div>
                    <div className="text-slate-300 font-mono text-[11px]">
                      {inspectionData.location.lat.toFixed(5)}°N, {inspectionData.location.lon.toFixed(5)}°E
                    </div>
                  </div>

                  {/* Terrain Attributes */}
                  <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800 space-y-1.5">
                    <div className="text-slate-400 text-[10px] uppercase font-mono tracking-wider mb-1">
                      Copernicus DEM 30m Morphometrics
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Elevation:</span>
                      <span className="font-semibold text-amber-300">
                        {formatFiniteNumber(inspectionData.terrain?.elevation_m, 2, "m ASL")}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Slope Angle:</span>
                      <span className="font-semibold text-orange-400">
                        {formatFiniteNumber(inspectionData.terrain?.slope_deg, 2, "°")}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Aspect Azimuth:</span>
                      <span className="font-semibold text-purple-300">
                        {formatFiniteNumber(inspectionData.terrain?.aspect_deg, 2, "°")}
                      </span>
                    </div>
                  </div>

                  {/* Susceptibility & Dynamic Hazard */}
                  <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800 space-y-1.5">
                    <div className="text-slate-400 text-[10px] uppercase font-mono tracking-wider mb-1">
                      XGBoost Model Predictions
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Susceptibility Rating:</span>
                      <span className="font-bold text-amber-400">
                        {inspectionData.susceptibility?.class_rating || "N/A"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">Probability:</span>
                      <span className="font-mono text-slate-200">
                        {inspectionData.susceptibility?.probability != null
                          ? (inspectionData.susceptibility.probability * 100).toFixed(1) + "%"
                          : "N/A"}
                      </span>
                    </div>
                    <div className="flex justify-between border-t border-slate-800 pt-1.5 mt-1.5">
                      <span className="text-slate-400">Dynamic Hazard Class:</span>
                      <span className="font-bold text-rose-400">
                        {inspectionData.dynamic_hazard?.hazard_class || "N/A"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-400">24h Rain Proxy:</span>
                      <span className="font-mono text-sky-400">
                        {formatFiniteNumber(inspectionData.dynamic_hazard?.rainfall_accum_24h_mm, 1, "mm")}
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    )}
  </MapErrorBoundary>
</div>
  );
}

export default MapContainer;
