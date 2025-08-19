type Activity = {
  title: string;
  category: "agri"|"transfo"|"artisanat"|"nature"|"social";
  duration: number;
  safety: 1|2;
  desc: string;
};

const activities: Activity[] = [
  { title:"Nourrir et soigner les moutons", category:"agri", duration:60, safety:1, desc:"Alimentation, eau, observation et bien-être du troupeau." },
  { title:"Tonte & entretien du troupeau", category:"agri", duration:90, safety:2, desc:"Hygiène, tonte (démonstration) et soins courants." },
  { title:"Soins basse-cour", category:"agri", duration:60, safety:1, desc:"Poules, canards, lapins : alimentation, abris, propreté." },
  { title:"Plantation de cultures", category:"agri", duration:90, safety:1, desc:"Semis, arrosage, paillage, suivi des jeunes plants." },
  { title:"Initiation maraîchage", category:"agri", duration:120, safety:1, desc:"Plan de culture, entretien, récolte respectueuse." },
  { title:"Gestion des clôtures & abris", category:"agri", duration:120, safety:2, desc:"Identifier, réparer et sécuriser parcs et abris." },

  { title:"Fabrication de fromage", category:"transfo", duration:90, safety:2, desc:"Du lait au caillé : hygiène, moulage, affinage (découverte)." },
  { title:"Confitures & conserves", category:"transfo", duration:90, safety:1, desc:"Préparation, stérilisation, mise en pot, étiquetage." },
  { title:"Transformation de la laine", category:"transfo", duration:90, safety:1, desc:"Lavage, cardage et petite création textile." },
  { title:"Fabrication de jus", category:"transfo", duration:90, safety:2, desc:"Du verger à la bouteille : tri, pressage, filtration." },
  { title:"Séchage d’herbes aromatiques", category:"transfo", duration:60, safety:1, desc:"Cueillette, séchage doux et conditionnement." },
  { title:"Pain au four à bois", category:"transfo", duration:120, safety:2, desc:"Pétrissage, façonnage, cuisson : respect des temps." },

  { title:"Construction d’abris", category:"artisanat", duration:120, safety:2, desc:"Petites structures bois : plan, coupe, assemblage." },
  { title:"Réparation & entretien des outils", category:"artisanat", duration:60, safety:1, desc:"Affûtage, graissage, vérifications simples." },
  { title:"Menuiserie simple", category:"artisanat", duration:120, safety:2, desc:"Mesure, coupe, ponçage, finitions." },
  { title:"Peinture & décoration d’espaces", category:"artisanat", duration:90, safety:1, desc:"Préparer, protéger, peindre proprement." },
  { title:"Aménagement d’espaces verts", category:"artisanat", duration:90, safety:1, desc:"Désherbage doux, paillage, plantations." },
  { title:"Panneaux & orientation", category:"artisanat", duration:90, safety:1, desc:"Concevoir et poser une signalétique claire." },

  { title:"Entretien de la rivière", category:"nature", duration:90, safety:2, desc:"Nettoyage doux, observation des berges." },
  { title:"Plantation d’arbres", category:"nature", duration:120, safety:1, desc:"Choix d’essences, tuteurage, paillage, suivi." },
  { title:"Potager écologique", category:"nature", duration:90, safety:1, desc:"Associations, paillis, rotation des cultures." },
  { title:"Compostage", category:"nature", duration:60, safety:1, desc:"Tri, compost et valorisation des déchets verts." },
  { title:"Observation de la faune locale", category:"nature", duration:60, safety:1, desc:"Discrétion, repérage, traces/indices." },
  { title:"Nichoirs & hôtels à insectes", category:"nature", duration:120, safety:1, desc:"Concevoir, fabriquer, installer des abris." },

  { title:"Journée portes ouvertes", category:"social", duration:180, safety:1, desc:"Préparer, accueillir, guider un public." },
  { title:"Visites guidées de la ferme", category:"social", duration:60, safety:1, desc:"Présenter la ferme et répondre simplement." },
  { title:"Ateliers pour enfants", category:"social", duration:90, safety:2, desc:"Jeux, découvertes nature, mini-gestes encadrés." },
  { title:"Cuisine collective (équipe)", category:"social", duration:90, safety:1, desc:"Préparer un repas simple et bon." },
  { title:"Goûter fermier", category:"social", duration:60, safety:1, desc:"Organisation, service, convivialité, propreté." },
  { title:"Participation à un marché local", category:"social", duration:180, safety:1, desc:"Stand, présentation, caisse symbolique (simulation)." }
];

const CAT_LABEL: Record<Activity["category"], string> = {
  agri: "Agriculture",
  transfo: "Transformation",
  artisanat: "Artisanat",
  nature: "Environnement",
  social: "Animation"
};

export default function ActivitesPage(){
  return (
    <main style={{padding:24, maxWidth:1100, margin:"0 auto"}}>
      <h1 style={{fontSize:28, fontWeight:800, marginBottom:8}}>Catalogue des 30 activités (interne MFR)</h1>
      <p style={{color:"#555", marginBottom:16}}>Consultation uniquement — aucun bouton d’inscription en ligne.</p>

      <div style={{display:"grid", gridTemplateColumns:"repeat(auto-fit,minmax(260px,1fr))", gap:12}}>
        {activities.map((a)=>(
          <article key={a.title} style={{border:"1px solid #eee", borderRadius:12, padding:12, background:"#fff"}}>
            <h3 style={{margin:"0 0 6px", fontWeight:700}}>{a.title}</h3>
            <p style={{margin:"0 0 8px", color:"#555"}}>{a.desc}</p>
            <div style={{display:"flex", gap:8, flexWrap:"wrap"}}>
              <span style={{fontSize:12, padding:"4px 8px", border:"1px solid #e5e7eb", borderRadius:999, background:"#fafafa"}}>{CAT_LABEL[a.category]}</span>
              <span style={{fontSize:12, padding:"4px 8px", border:"1px solid #e5e7eb", borderRadius:999, background:"#fafafa"}}>{a.duration} min</span>
              <span style={{
                fontSize:12, padding:"4px 8px", border:"1px solid #e5e7eb", borderRadius:999,
                background: a.safety===1 ? "#ecfdf5" : "#fff7ed",
                color: a.safety===1 ? "#065f46" : "#9a3412"
              }}>
                Sécurité : {a.safety}
              </span>
            </div>
          </article>
        ))}
      </div>
    </main>
  );
}
