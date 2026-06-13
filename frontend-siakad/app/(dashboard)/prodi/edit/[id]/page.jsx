// app/(dashboard)/prodi/edit/[id]/page.jsx
"use client";
import { use, useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchWithRefresh } from "@/app/lib/api";

export default function EditProdi({ params }) {
  const { id } = use(params); // Mendapatkan ID prodi dari parameter URL
  const [nama, setNama] = useState("");
  const [fakultas, setFakultas] = useState("");
  const router = useRouter();

  // Mengambil data lama untuk diisi ke dalam form
  useEffect(() => {
    const fetchDataProdi = async (id) => {
      try {
        const res = await fetchWithRefresh(`/api/prodi/${id}`, {
          method: "GET",
        });
        const result = await res.json();
        console.log(result);
        setNama(result.data?.nama ?? "");
        setFakultas(result.data?.fakultas ?? "");
      } catch (err) {
        console.error("Gagal mengambil data", err);
      }
    };
    fetchDataProdi(id);
  }, [id]);

  const handleUpdate = async (e) => {
    e.preventDefault();
    // Memanggil endpoint PUT /prodi/{id}
    const response = await fetchWithRefresh(`/api/prodi/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nama, fakultas }),
    });

    if (response.ok) {
      alert("Data berhasil diperbarui");
      router.push("/prodi"); // Kembali ke halaman utama dashboard
    } else {
      const err = await response.json();
      alert("Gagal memperbarui: " + (err.detail || "Terjadi kesalahan"));
    }
  };

  return (
    <div className="p-8 max-w-md mx-auto text-black mt-10 bg-white shadow-md rounded">
      <h2 className="text-2xl font-bold mb-6">Edit Program Studi</h2>
      <form onSubmit={handleUpdate}>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            ID Prodi (Tidak dapat diubah)
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border rounded bg-gray-100"
            value={id}
            disabled
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Nama Prodi
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border rounded"
            required
            value={nama}
            onChange={(e) => setNama(e.target.value)}
          />
        </div>
        <div className="mb-6">
          <label className="block text-gray-700 text-sm font-bold mb-2">
            Fakultas
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border rounded"
            required
            value={fakultas}
            onChange={(e) => setFakultas(e.target.value)}
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
            href="/prodi"
            className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 text-center flex-1"
          >
            Batal
          </Link>
        </div>
      </form>
    </div>
  );
}
