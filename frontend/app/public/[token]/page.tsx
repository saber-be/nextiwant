"use client";

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { claimWishlist, fetchPublicWishlist } from '../../../lib/wishlists';

export default function PublicWishlistPage() {
  const params = useParams<{ token: string }>();
  const token = params?.token;
  const [data, setData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [claiming, setClaiming] = useState(false);

  useEffect(() => {
    if (!token) return;
    (async () => {
      try {
        const res = await fetchPublicWishlist(token);
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, [token]);

  const handleClaim = async () => {
    if (!token) return;
    setClaiming(true);
    try {
      await claimWishlist(token);
      // In a full app you might redirect to dashboard here
    } catch (err) {
      console.error(err);
    } finally {
      setClaiming(false);
    }
  };

  if (loading) {
    return <p>Loading…</p>;
  }

  if (!data || !data.wishlist) {
    return <p>Public wishlist not found.</p>;
  }

  const { wishlist, share } = data;

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">{wishlist.name}</h1>
          {wishlist.description && <p className="text-sm text-slate-300">{wishlist.description}</p>}
        </div>
        {share?.is_claimable && (
          <button
            type="button"
            disabled={claiming}
            onClick={handleClaim}
            className="rounded bg-sky-600 px-3 py-1 text-sm font-semibold text-white hover:bg-sky-500 disabled:opacity-60"
          >
            {claiming ? 'Claiming…' : 'Claim wishlist'}
          </button>
        )}
      </div>

      <ul className="space-y-2 text-sm">
        {wishlist.items?.map((item: any) => (
          <li key={item.id} className="rounded border border-slate-800 bg-slate-900 px-3 py-2">
            <div className="font-medium">{item.title}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}
