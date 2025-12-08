// // src/api.js
// const API_BASE_URL = import.meta.env.VITE_API_URL;

// export async function fetchFromAPI(endpoint, options = {}) {
//   const res = await fetch(`${API_BASE_URL}${endpoint}`, options);
//   if (!res.ok) {
//     throw new Error(`API error: ${res.status}`);
//   }
//   return res.json();
// }
// src/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL;

export async function fetchFromAPI(endpoint, options = {}) {
  // Ensure exactly ONE slash between base and endpoint
  const url = API_BASE_URL.endsWith("/")
    ? API_BASE_URL + endpoint
    : API_BASE_URL + "/" + endpoint;

  const res = await fetch(url, options);

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error: ${res.status} - ${text}`);
  }

  return res.json();
}
