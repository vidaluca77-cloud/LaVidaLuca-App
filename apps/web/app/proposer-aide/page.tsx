"use client";
import React from "react";

export default function ProposerAide() {
  return (
    <main style={{ maxWidth: 800, margin: "40px auto", padding: 16 }}>
      <h1>Proposer mon aide</h1>
      <p>Si vous souhaitez contribuer au projet (temps, matériel, compétences), laissez vos coordonnées ci-dessous.</p>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          alert("Merci ! Nous vous recontactons rapidement.");
        }}
        style={{ display: "grid", gap: 12, marginTop: 16 }}
      >
        <input name="nom" placeholder="Votre nom" required style={{ padding: 10, border: "1px solid #ddd", borderRadius: 6 }} />
        <input name="email" type="email" placeholder="Votre email" required style={{ padding: 10, border: "1px solid #ddd", borderRadius: 6 }} />
        <input name="telephone" placeholder="Votre téléphone (optionnel)" style={{ padding: 10, border: "1px solid #ddd", borderRadius: 6 }} />
        <textarea name="message" placeholder="Que souhaitez-vous proposer ?" rows={5} style={{ padding: 10, border: "1px solid #ddd", borderRadius: 6 }} />
        <button type="submit" style={{ padding: "10px 14px" }}>Envoyer</button>
      </form>
    </main>
  );
}
