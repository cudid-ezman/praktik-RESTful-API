// app/(dashboard)/fakultas/tambah/page.jsx
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchWithRefresh } from "@/app/lib/api";

export default function TambahFakultas() {
  const [id, setId] = useState("");
  const [nama, setNama] = useState("");
  const router = useRouter();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetchWithRefresh("http://127.0.0.1:8000/fakultas/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id, nama }),
    });

    if (response.ok) {
      alert("Data fakultas berhasil disimpan");
      router.push("/fakultas"); // Kembali ke dashboard fakultas
    } else {
      const err = await response.json();
      alert("Gagal: " + (err.detail || "Terjadi kesalahan"));
    }
  };

  return (
    <div className="p-8 max-w-md mx-auto text-black mt-10 bg-white shadow-md rounded">
      <h2 className="text-2xl font-bold mb-6">Tambah Data Fakultas</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            ID Fakultas (cth: FST)
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border rounded"
            required
            value={id}
            onChange={(e) => setId(e.target.value)}
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Nama Fakultas
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border rounded"
            required
            value={nama}
            onChange={(e) => setNama(e.target.value)}
          />
        </div>
        <div className="flex gap-4">
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 flex-1"
          >
            Simpan
          </button>
          <Link
            href="/fakultas"
            className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 text-center flex-1"
          >
            Batal
          </Link>
        </div>
      </form>
    </div>
  );
}
