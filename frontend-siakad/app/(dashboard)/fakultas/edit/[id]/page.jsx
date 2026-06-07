// app/(dashboard)/fakultas/edit/[id]/page.jsx
"use client";
import { use, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchWithRefresh } from "@/app/lib/api";

export default function EditFakultas({ params }) {
  const { id } = use(params); // Menangkap ID dari URL
  const [nama, setNama] = useState("");
  const router = useRouter();

  // Ambil data fakultas yang lama untuk mengisi form
  useEffect(() => {
    const fetchDataFakultas = async (id) => {
      try {
        const res = await fetchWithRefresh(
          `http://127.0.0.1:8000/fakultas/${id}`,
          {
            method: "GET",
          },
        );
        const result = await res.json();
        setNama(result.data?.nama ?? "");
      } catch (err) {
        console.error("Gagal mengambil data fakultas", err);
      }
    };
    fetchDataFakultas(id);
  }, [id]);

  const handleUpdate = async (e) => {
    e.preventDefault();
    const response = await fetchWithRefresh(
      `http://127.0.0.1:8000/fakultas/${id}`,
      {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nama }), // Hanya nama yang bisa diubah
      },
    );

    if (response.ok) {
      alert("Data fakultas berhasil diperbarui");
      router.push("/fakultas"); // Kembali ke dashboard fakultas
    } else {
      const err = await response.json();
      alert("Gagal memperbarui: " + (err.detail || "Terjadi kesalahan"));
    }
  };

  return (
    <div className="p-8 max-w-md mx-auto text-black mt-10 bg-white shadow-md rounded">
      <h2 className="text-2xl font-bold mb-6">Edit Data Fakultas</h2>
      <form onSubmit={handleUpdate}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            ID Fakultas (Tidak dapat diubah)
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border rounded bg-gray-100 cursor-not-allowed"
            value={id}
            disabled
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
            className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600 flex-1"
          >
            Update
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
