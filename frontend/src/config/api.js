const API_BASE_URL = (
    import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
  ).replace(/\/$/, "");
  
  export { API_BASE_URL };
  
  export const API_ENDPOINTS = {
    health: "/health",
    jobs: "/jobs",
    analyze: "/analyze",
  };
  
  export async function apiFetch(path, options = {}) {
    const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  
    return fetch(`${API_BASE_URL}${normalizedPath}`, options);
  }