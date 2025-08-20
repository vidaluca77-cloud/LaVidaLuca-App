import Link from "next/link";

export default function NotFound() {
  return (
    <div style={{ padding: "32px", textAlign: "center" }}>
      <h1>404 - Page Non Trouvée</h1>
      <p>La page que vous recherchez n&apos;existe pas.</p>
      <Link 
        href="/" 
        style={{ 
          color: "#0070f3", 
          textDecoration: "underline" 
        }}
      >
        Retour à l&apos;accueil
      </Link>
    </div>
  );
}