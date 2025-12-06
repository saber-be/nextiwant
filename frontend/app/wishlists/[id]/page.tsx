"use client";

import { useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import { addWishlistItem, fetchWishlist, fetchPublicWishlist, createShare } from '../../../lib/wishlists';

export default function WishlistDetailPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [wishlist, setWishlist] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState('');
  const [creating, setCreating] = useState(false);
  const [shareLink, setShareLink] = useState('');

  useEffect(() => {
    if (!id) return;
    (async () => {
      try {
        const wl = await fetchWishlist(id);
        setWishlist(wl);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!id || !title.trim()) return;
    setCreating(true);
    try {
      const item = await addWishlistItem(id, { title });
      setWishlist((prev: any) => ({ ...prev, items: [...(prev?.items ?? []), item] }));
      setTitle('');
    } catch (err) {
      console.error(err);
    } finally {
      setCreating(false);
    }
  };

  const handleShare = async () => {
    if (!id || !wishlist) return;
    try {
      const share = await createShare(id, { is_claimable: true });
      const url = `${window.location.origin}/public/${share.token}`;
      setShareLink(url);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return <p>Loading wishlist…</p>;
  }

  if (!wishlist) {
    return <p>Wishlist not found.</p>;
  }

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">{wishlist.name}</h1>
          {wishlist.description && <p className="text-sm text-slate-300">{wishlist.description}</p>}
        </div>
        <button
          type="button"
          onClick={handleShare}
          className="rounded bg-sky-600 px-3 py-1 text-sm font-semibold text-white hover:bg-sky-500"
        >
          Share
        </button>
      </div>

      {shareLink && (
        <div className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-xs text-slate-200">
          Public link: <a href={shareLink} className="text-sky-400 hover:underline">{shareLink}</a>
        </div>
      )}

      <form onSubmit={handleAddItem} className="flex gap-2 max-w-md">
        <input
          className="flex-1 rounded border border-slate-700 bg-slate-900 px-3 py-2 text-sm"
          placeholder="New item title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button
          type="submit"
          disabled={creating}
          className="rounded bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-500 disabled:opacity-60"
        >
          {creating ? 'Adding…' : 'Add'}
        </button>
      </form>

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
