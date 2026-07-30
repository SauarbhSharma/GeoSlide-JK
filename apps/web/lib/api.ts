// Centralized API configuration for GeoSlide-JK
// In production: NEXT_PUBLIC_API_BASE_URL is empty string = same-origin relative paths
// Next.js rewrites handle /api/* → FastAPI backend
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? '';

export function apiUrl(path: string): string {
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  if (!API_BASE_URL) {
    return cleanPath; // same-origin relative path
  }
  return `${API_BASE_URL}${cleanPath}`;
}
