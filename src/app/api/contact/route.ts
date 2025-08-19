import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    
    // TODO: Intégrer avec un service d'email ou Discord
    console.log("Contact form submission:", body);
    
    // TODO: Optionnel - utiliser l'API IA pour analyser le message
    // const iaApiUrl = process.env.NEXT_PUBLIC_IA_API_URL;
    // if (iaApiUrl) {
    //   // Analyser le message avec l'IA pour catégorisation automatique
    // }
    
    return NextResponse.json({ 
      success: true, 
      message: "Votre message a été envoyé avec succès." 
    });
  } catch (error) {
    console.error("Contact form error:", error);
    return NextResponse.json(
      { success: false, message: "Erreur lors de l'envoi du message." },
      { status: 500 }
    );
  }
}
