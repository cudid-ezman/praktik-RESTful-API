// app/lib/api.js
export async function refreshAccessToken() {
  try {
    const response = await fetch("http://127.0.0.1:8000/refresh", {
      method: "POST",
      credentials: "include", // Supaya cookie refresh_token ikut terkirim
    });
    return response.ok;
  } catch (err) {
    return false;
  }
}

export async function fetchWithRefresh(url, options = {}) {
  const baseOptions = {
    credentials: "include",
    ...options,
  };

  let response;
  try {
    response = await fetch(url, baseOptions);
  } catch (err) {
    if (typeof window !== "undefined") window.location.href = "/login";
    throw err;
  }

  // Jika access_token kedaluwarsa (401) atau dilarang (403)
  if (response.status === 401 || response.status === 403) {
    const refreshed = await refreshAccessToken();
    if (!refreshed) {
      if (typeof window !== "undefined") window.location.href = "/login";
      throw new Error("Session expired. Please login again.");
    }
    // Jika refresh berhasil, ulangi fetch ke URL awal dengan access_token baru
    response = await fetch(url, baseOptions);
    if (response.status === 401 || response.status === 403) {
      if (typeof window !== "undefined") window.location.href = "/login";
      throw new Error("Session expired. Please login again.");
    }
  }
  return response;
}
