import { NextResponse } from "next/server";
import { submitContactMessage } from "@/lib/supabase";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    
    // Validate required fields
    if (!body.name || !body.email || !body.message) {
      return NextResponse.json(
        { error: "Nom, email et message requis" },
        { status: 400 }
      );
    }

    // Submit to Supabase
    const { data, error } = await submitContactMessage({
      name: body.name,
      email: body.email,
      phone: body.phone || null,
      message: body.message,
      type: body.type || 'general'
    });

    if (error) {
      console.error("Contact submission error:", error);
      return NextResponse.json(
        { error: "Erreur lors de l'envoi du message" },
        { status: 500 }
      );
    }

    console.log("Contact message submitted:", data);
    return NextResponse.json({ ok: true, message: "Message envoyé avec succès" });
  } catch (error) {
    console.error("Contact API error:", error);
    return NextResponse.json(
      { error: "Erreur serveur" },
      { status: 500 }
    );
  }
}
