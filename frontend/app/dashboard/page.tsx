"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { createWishlist, fetchMyWishlists } from '../../lib/wishlists';

export default function DashboardPage() {
  const [wishlists, setWishlists] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const data = await fetchMyWishlists();
        setWishlists(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setCreating(true);
    try {
      const wl = await createWishlist({ name });
      setWishlists((prev) => [...prev, wl]);
      setName('');
    } catch (err) {
      console.error(err);
    } finally {
      setCreating(false);
    }
  };

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">My wishlists</h1>
      </div>

      <form onSubmit={handleCreate} className="flex gap-2 max-w-md">
        <input
          className="flex-1 rounded border border-slate-700 bg-slate-900 px-3 py-2 text-sm"
          placeholder="New wishlist name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button
          type="submit"
          disabled={creating}
          className="rounded bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-500 disabled:opacity-60"
        >
          {creating ? 'Creating…' : 'Create'}
        </button>
      </form>

      {loading ? (
        <p>Loading…</p>
      ) : wishlists.length === 0 ? (
        <p className="text-sm text-slate-300">No wishlists yet.</p>
      ) : (
        <ul className="space-y-2">
          {wishlists.map((wl) => (
            <li key={wl.id} className="rounded border border-slate-800 bg-slate-900 px-3 py-2 text-sm">
              <Link href={`/wishlists/${wl.id}`} className="font-medium text-sky-400 hover:underline">
                {wl.name}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
