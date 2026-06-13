// app/(dashboard)/fakultas/page.jsx
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchWithRefresh } from "@/app/lib/api";

export default function DashboardFakultas() {
  const [fakultasList, setFakultasList] = useState([]);
  const [user, setUser] = useState("Admin");
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const router = useRouter();

  useEffect(() => {
    const loadData = async () => {
      try {
        const resAuth = await fetchWithRefresh("/api/profil");
        if (!resAuth.ok) throw new Error(`HTTP ${resAuth.status}`);
        const authData = await resAuth.json();
        setUser(authData.data_login.username);

        // Fetch data tabel fakultas
        const resFakultas = await fetchWithRefresh("/api/fakultas/");
        if (!resFakultas.ok) {
          throw new Error(`HTTP ${resFakultas.status}`);
        }
        const dataFak = await resFakultas.json();
        setFakultasList(dataFak.data);
      } catch (err) {
        console.error(err);
        router.push("/login");
      }
    };
    loadData();
  }, [refreshTrigger, router]);

  const handleDelete = async (id) => {
    if (!confirm("Yakin ingin menghapus data fakultas ini?")) return;
    try {
      const res = await fetchWithRefresh(`/api/fakultas/${id}`, {
        method: "DELETE",
      });
      if (res.ok) {
        setRefreshTrigger((prev) => prev + 1);
      } else {
        alert("Gagal menghapus data");
      }
    } catch (err) {
      console.error(err);
      alert("Terjadi kesalahan jaringan saat menghapus");
    }
  };

  const handleLogout = async () => {
    try {
      const res = await fetch("/api/logout", {
        method: "POST",
        credentials: "include",
      });
      if (res.ok) {
        router.push("/login");
      } else {
        alert("Gagal logout dari server");
      }
    } catch (err) {
      console.error(err);
      alert("Terjadi kesalahan jaringan saat logout");
    }
  };

  if (!user) return <p className="text-center mt-20 text-black">Loading...</p>;

  return (
    <div className="p-8 max-w-4xl mx-auto text-black">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Dashboard Fakultas</h1>
        <div className="flex gap-4 items-center">
          <span>Halo, {user}</span>
          <button
            onClick={handleLogout}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Logout
          </button>
        </div>
      </div>

      <div className="mb-4 flex gap-4">
        <Link
          href="/fakultas/tambah"
          className="bg-green-500 text-white px-4 py-2 rounded inline-block hover:bg-green-600"
        >
          + Tambah Fakultas
        </Link>
        {/* Tombol navigasi kembali ke halaman Prodi */}
        <Link
          href="/prodi"
          className="bg-gray-500 text-white px-4 py-2 rounded inline-block hover:bg-gray-600"
        >
          Lihat Data Prodi
        </Link>
      </div>

      <table className="w-full bg-white shadow-md rounded border">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-3 border">ID Fakultas</th>
            <th className="p-3 border">Nama Fakultas</th>
            <th className="p-3 border">Aksi</th>
          </tr>
        </thead>
        <tbody>
          {fakultasList.map((fak) => (
            <tr key={fak.id} className="text-center hover:bg-gray-50">
              <td className="p-3 border">{fak.id}</td>
              <td className="p-3 border">{fak.nama}</td>
              <td className="p-3 border flex justify-center gap-2">
                <Link
                  href={`/fakultas/edit/${fak.id}`}
                  className="bg-yellow-500 text-white px-3 py-1 rounded text-sm hover:bg-yellow-600"
                >
                  Edit
                </Link>
                <button
                  onClick={() => handleDelete(fak.id)}
                  className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                >
                  Hapus
                </button>
              </td>
            </tr>
          ))}
          {fakultasList.length === 0 && (
            <tr>
              <td colSpan="3" className="p-4 text-center">
                Data masih kosong
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
