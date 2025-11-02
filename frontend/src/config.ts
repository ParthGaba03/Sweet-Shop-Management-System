// API Configuration
// In production, set REACT_APP_API_URL environment variable
// For local development, uses proxy from package.json or defaults to localhost
const API_URL = process.env.REACT_APP_API_URL || '';

// Export API base URL
// If API_URL is set, use it; otherwise, use relative paths (proxy will handle it in dev)
export const API_BASE_URL = API_URL;

// Helper function to create full API URL
export const getApiUrl = (endpoint: string): string => {
  if (API_BASE_URL) {
    // Remove trailing slash from API_BASE_URL and leading slash from endpoint
    const base = API_BASE_URL.replace(/\/$/, '');
    const path = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    return `${base}${path}`;
  }
  // In development, use relative paths (proxy will handle routing)
  return endpoint;
};

