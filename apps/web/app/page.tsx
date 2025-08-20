export default function Home() {
  return (
    <main style={{ padding: "32px", maxWidth: 900, margin: "0 auto" }}>
      <h1 style={{ fontSize: 36, fontWeight: 800, marginBottom: 8 }}>
        Le cœur avant l’économie
      </h1>

      <p style={{ fontSize: 18, color: "#555", marginBottom: 16 }}>
        La Vida Luca — former les jeunes en MFR, développer une agriculture vivante
        et redonner un avenir au monde rural.
      </p>

      <nav style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
        <a
          href="/activites"
          style={{
            padding: "10px 14px",
            border: "1px solid #ddd",
            borderRadius: 6,
          }}
        >
          Voir les activités
        </a>

        <a
          href="/proposer-aide"
          style={{
            padding: "10px 14px",
            border: "1px solid #ddd",
            borderRadius: 6,
          }}
        >
          Proposer une aide
        </a>

        <a
          href="/gamification"
          style={{
            padding: "10px 14px",
            border: "1px solid #10b981",
            borderRadius: 6,
            background: "#10b981",
            color: "white",
          }}
        >
          🎮 Gamification
        </a>

        <a
          href="/test-ia"
          style={{
            padding: "10px 14px",
            border: "1px solid #0070f3",
            borderRadius: 6,
            background: "#0070f3",
            color: "white",
          }}
        >
          Tester l’IA
        </a>
      </nav>
    </main>
  );
}
