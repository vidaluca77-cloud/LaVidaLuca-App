"use client";
import { useMemo, useState } from "react";

type Item = {
  id: string;
  title: string;
  description: string;
  price: string;
  category:
    | "Produits vivants"
    | "Activités terrain"
    | "Services"
    | "Dons en nature";
  departement: string;
  img?: string;
  tags: string[];
};

const DATA: Item[] = [
  {
    id: "agn-001",
    title: "Agneau broutard (vivant)",
    description: "Réservation locale, qualité élevée.",
    price: "299 € TTC",
    category: "Produits vivants",
    departement: "Calvados (14)",
    tags: ["local", "réservation"],
  },
  {
    id: "jour-001",
    title: "Journée découverte ferme",
    description: "Publics jeunes, familles, structures.",
    price: "Prix libre",
    category: "Activités terrain",
    departement: "Calvados (14)",
    tags: ["groupes"],
  },
  {
    id: "plant-001",
    title: "Plants & arbres (saison)",
    description: "Variétés locales selon stock.",
    price: "Selon stock",
    category: "Produits vivants",
    departement: "Calvados (14)",
    tags: ["pépinière"],
  },
  {
    id: "srv-001",
    title: "Visite pédagogique MFR/lycées",
    description: "Accueil encadré, objectifs pédagogiques.",
    price: "Sur devis",
    category: "Services",
    departement: "Calvados (14)",
    tags: ["éducation"],
  },
  {
    id: "don-001",
    title: "Dons en nature",
    description: "Matériel agricole, plants, clôtures, caméras…",
    price: "—",
    category: "Dons en nature",
    departement: "National",
    tags: ["partenariat"],
  },
];

const CATEGORIES = [
  "Toutes",
  "Produits vivants",
  "Activités terrain",
  "Services",
  "Dons en nature",
] as const;

export default function Catalogue() {
  const [q, setQ] = useState("");
  const [cat, setCat] = useState<(typeof CATEGORIES)[number]>("Toutes");

  const items = useMemo(() => {
    return DATA.filter((it) => {
      const okCat = cat === "Toutes" || it.category === cat;
      const okQ = (
        it.title +
        it.description +
        it.departement +
        it.tags.join(" ")
      )
        .toLowerCase()
        .includes(q.toLowerCase());
      return okCat && okQ;
    });
  }, [q, cat]);

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Catalogue</h1>
        <p className="opacity-80">
          Sélectionne une catégorie ou cherche un mot-clé.
        </p>
      </header>

      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Rechercher…"
          className="w-full rounded border px-3 py-2"
        />
        <select
          value={cat}
          onChange={(e) => setCat(e.target.value as any)}
          className="rounded border px-3 py-2"
        >
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      {items.length === 0 ? (
        <div className="rounded border p-6">Aucun résultat.</div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {items.map((it) => (
            <div key={it.id} className="rounded-lg border p-5 flex flex-col">
              <div className="h-40 w-full rounded bg-gray-100 mb-4 flex items-center justify-center text-sm opacity-60">
                Image
              </div>
              <h3 className="font-semibold">{it.title}</h3>
              <p className="mt-1 text-sm opacity-80">{it.description}</p>
              <div className="mt-3 text-sm font-medium">{it.price}</div>
              <div className="mt-2 text-xs opacity-70">{it.departement}</div>
              <div className="mt-3 flex flex-wrap gap-2">
                {it.tags.map((t) => (
                  <span key={t} className="rounded border px-2 py-1 text-xs">
                    {t}
                  </span>
                ))}
              </div>
              <a
                href="/contact"
                className="mt-4 inline-block rounded bg-emerald-500 px-4 py-2 text-white text-center"
              >
                Contacter
              </a>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
