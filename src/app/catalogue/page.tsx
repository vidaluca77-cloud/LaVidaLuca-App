"use client";
import { useMemo, useState } from "react";
import { Button, Input, Card } from '@/components/ui';

type Item = {
  id: string;
  title: string;
  description: string;
  price: string;
  category: "Produits vivants" | "Activités terrain" | "Services" | "Dons en nature";
  departement: string;
  img?: string;
  tags: string[];
};

const DATA: Item[] = [
  { id:"agn-001", title:"Agneau broutard (vivant)", description:"Réservation locale, qualité élevée.", price:"299 € TTC", category:"Produits vivants", departement:"Calvados (14)", tags:["local","réservation"] },
  { id:"jour-001", title:"Journée découverte ferme", description:"Publics jeunes, familles, structures.", price:"Prix libre", category:"Activités terrain", departement:"Calvados (14)", tags:["groupes"] },
  { id:"plant-001", title:"Plants & arbres (saison)", description:"Variétés locales selon stock.", price:"Selon stock", category:"Produits vivants", departement:"Calvados (14)", tags:["pépinière"] },
  { id:"srv-001", title:"Visite pédagogique MFR/lycées", description:"Accueil encadré, objectifs pédagogiques.", price:"Sur devis", category:"Services", departement:"Calvados (14)", tags:["éducation"] },
  { id:"don-001", title:"Dons en nature", description:"Matériel agricole, plants, clôtures, caméras…", price:"—", category:"Dons en nature", departement:"National", tags:["partenariat"] },
];

const CATEGORIES = ["Toutes","Produits vivants","Activités terrain","Services","Dons en nature"] as const;

export default function Catalogue() {
  const [q, setQ] = useState("");
  const [cat, setCat] = useState<typeof CATEGORIES[number]>("Toutes");

  const items = useMemo(() => {
    return DATA.filter(it => {
      const okCat = cat === "Toutes" || it.category === cat;
      const okQ = (it.title + it.description + it.departement + it.tags.join(" "))
        .toLowerCase().includes(q.toLowerCase());
      return okCat && okQ;
    });
  }, [q, cat]);

  return (
    <div className="space-y-8">
      <header className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Catalogue</h1>
        <p className="text-gray-600 mt-2">Découvrez nos produits, services et opportunités de partenariat.</p>
      </header>

      <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
        <Input
          value={q}
          onChange={setQ}
          placeholder="Rechercher…"
          className="flex-1"
        />
        <select
          value={cat}
          onChange={e => setCat(e.target.value as typeof CATEGORIES[number])}
          className="px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-vida-green focus:border-transparent"
        >
          {CATEGORIES.map(c => (
            <option key={c} value={c}>{c}</option>
          ))}
        </select>
      </div>

      <div className="text-sm text-gray-600">
        {items.length} résultat{items.length > 1 ? 's' : ''} trouvé{items.length > 1 ? 's' : ''}
      </div>

      {items.length === 0 ? (
        <Card className="text-center py-12">
          <p className="text-gray-500">Aucun résultat trouvé pour cette recherche.</p>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {items.map(item => (
            <Card key={item.id} hover>
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <span className="bg-vida-green/10 text-vida-green px-2 py-1 rounded-full text-xs font-medium">
                    {item.category}
                  </span>
                  <span className="text-sm text-gray-500">{item.departement}</span>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{item.title}</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">{item.description}</p>
                </div>

                <div className="flex flex-wrap gap-1">
                  {item.tags.map((tag, i) => (
                    <span key={i} className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">
                      {tag}
                    </span>
                  ))}
                </div>

                <div className="flex items-center justify-between pt-4 border-t">
                  <span className="font-semibold text-vida-green">{item.price}</span>
                  <Button size="sm">
                    {item.category === 'Dons en nature' ? 'Proposer' : 'Commander'}
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
