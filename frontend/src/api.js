// src/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL;

export async function fetchFromAPI(endpoint, options = {}) {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, options);
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}
