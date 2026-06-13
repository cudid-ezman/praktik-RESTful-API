// app/(dashboard)/prodi/page.jsx
"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchWithRefresh } from "@/app/lib/api";

export default function Dashboard() {
  const [prodiList, setProdiList] = useState([]);
  const [user, setUser] = useState("Admin");
  // 1. Buat state baru sebagai "pelatuk" (trigger) untuk memuat ulang data
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const router = useRouter();

  // 2. Masukkan logika fetch langsung ke dalam useEffect
  useEffect(() => {
    const loadData = async () => {
      try {
        // UBAH 1: Fetch profil diarahkan langsung ke localhost:8000
        const resAuth = await fetchWithRefresh("http://localhost:8000/profil");
        if (!resAuth.ok) throw new Error(`HTTP ${resAuth.status}`);
        const authData = await resAuth.json();
        setUser(authData.data.username);

        // UBAH 2: Fetch data tabel prodi diarahkan langsung ke localhost:8000/prodi/
        const resProdi = await fetchWithRefresh("http://localhost:8000/prodi/");
        if (!resProdi.ok) {
          console.error(
            "fetch /prodi failed",
            resProdi.status,
            resProdi.statusText,
          );
          throw new Error(`HTTP ${resProdi.status}`);
        }
        const dataProdi = await resProdi.json();
        setProdiList(dataProdi.data);
      } catch (err) {
        console.error(err);
        router.push("/login");
      }
    };
    loadData();
  }, [refreshTrigger, router]); // 3. useEffect berjalan saat pertama kali dimuat & saat refreshTrigger berubah

  const handleDelete = async (id) => {
    if (!confirm("Yakin ingin menghapus data ini?")) return;
    try {
      // UBAH 3: Delete diarahkan langsung ke localhost:8000
      const res = await fetchWithRefresh(`http://localhost:8000/prodi/${id}`, {
        method: "DELETE",
      });
      if (res.ok) {
        // 4. Ubah nilai trigger agar useEffect berjalan ulang untuk refresh tabel!
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
      // UBAH 4: Logout diarahkan langsung ke localhost:8000
      const res = await fetch("http://localhost:8000/logout", {
        method: "POST",
        credentials: "include", // Wajib agar cookie dikirim ke server untuk dihapus
      });
      if (res.ok) {
        router.push("/login"); // Kembali ke halaman login
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
        <h1 className="text-3xl font-bold">Dashboard Admin</h1>
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

      <div className="mb-4">
        <Link
          href="/prodi/tambah"
          className="bg-green-500 text-white px-4 py-2 rounded inline-block hover:bg-green-600"
        >
          + Tambah Prodi
        </Link>
      </div>

      <table className="w-full bg-white shadow-md rounded border">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-3 border">ID Prodi</th>
            <th className="p-3 border">Nama Program Studi</th>
            <th className="p-3 border">Fakultas</th>
            <th className="p-3 border">Aksi</th>
          </tr>
        </thead>
        <tbody>
          {prodiList.map((prodi) => (
            <tr key={prodi.id} className="text-center hover:bg-gray-50">
              <td className="p-3 border">{prodi.id}</td>
              <td className="p-3 border">{prodi.nama}</td>
              <td className="p-3 border">{prodi.fakultas}</td>
              <td className="p-3 border flex justify-center gap-2">
                <Link
                  href={`/prodi/edit/${prodi.id}`}
                  className="bg-yellow-500 text-white px-3 py-1 rounded text-sm hover:bg-yellow-600"
                >
                  Edit
                </Link>
                <button
                  onClick={() => handleDelete(prodi.id)}
                  className="bg-red-500 text-white px-3 py-1 rounded text-sm hover:bg-red-600"
                >
                  Hapus
                </button>
              </td>
            </tr>
          ))}
          {prodiList.length === 0 && (
            <tr>
              <td colSpan="4" className="p-4 text-center">
                Data masih kosong
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}