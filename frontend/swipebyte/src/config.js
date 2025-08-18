export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || window.location.origin; // empty => same-origin

// Helper if you centralize paths:
export const API = (path) =>
  (API_BASE_URL ? API_BASE_URL.replace(/\/$/, "") : "") +
  (path.startsWith("/") ? path : "/" + path);

/** Build absolute API URLs safely */
export const apiUrl = (p) => new URL(p, API_BASE_URL || window.location.origin).toString();
