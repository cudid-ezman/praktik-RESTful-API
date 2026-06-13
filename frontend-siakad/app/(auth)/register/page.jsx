// app/(auth)/register/page.jsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const router = useRouter();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    try {
      // UBAH: Arahkan fetch langsung ke localhost:8000
      const response = await fetch("http://localhost:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        setSuccess("Registrasi berhasil, mengalihkan ke halaman login...");
        // Beri jeda 2 detik agar pesan sukses terbaca sebelum pindah halaman
        setTimeout(() => {
          router.push("/login");
        }, 2000);
      } else {
        const errData = await response.json();
        setError(errData.detail || "Registrasi gagal");
      }
    } catch (err) {
      setError("Terjadi kesalahan koneksi ke server");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <form
        onSubmit={handleRegister}
        className="bg-white p-8 rounded shadow-md w-96"
      >
        <h2 className="text-2xl font-bold mb-6 text-center text-black">
          Register SIAKAD
        </h2>

        {error && (
          <p className="text-red-500 mb-4 text-sm text-center">{error}</p>
        )}
        {success && (
          <p className="text-green-500 mb-4 text-sm text-center">{success}</p>
        )}

        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Username
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border rounded text-black"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Password
          </label>
          <input
            type="password"
            className="w-full px-3 py-2 border rounded text-black"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-green-500 text-white font-bold py-2 px-4 rounded hover:bg-green-600 mb-4"
        >
          Register
        </button>
        <p className="text-center text-sm text-black">
          Sudah punya akun?{" "}
          <Link href="/login" className="text-blue-500 hover:underline">
            Login di sini
          </Link>
        </p>
      </form>
    </div>
  );
}
