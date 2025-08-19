"use client";
import { useState } from "react";

export default function Contact() {
  const [ok, setOk] = useState(false);
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.currentTarget) as any);
    await fetch("/api/contact", { method: "POST", body: JSON.stringify(data) });
    setOk(true);
  }
  return (
    <div className="max-w-xl">
      <h1 className="text-3xl font-bold mb-4">Contact</h1>
      {ok ? (
        <p>Merci ! On te répond vite.</p>
      ) : (
        <form onSubmit={onSubmit} className="space-y-3">
          <input
            name="name"
            placeholder="Nom"
            className="w-full border px-3 py-2 rounded"
            required
          />
          <input
            name="email"
            type="email"
            placeholder="Email"
            className="w-full border px-3 py-2 rounded"
            required
          />
          <textarea
            name="message"
            placeholder="Ton message"
            className="w-full border px-3 py-2 rounded h-28"
            required
          />
          <button className="border px-4 py-2 rounded">Envoyer</button>
        </form>
      )}
    </div>
  );
}
