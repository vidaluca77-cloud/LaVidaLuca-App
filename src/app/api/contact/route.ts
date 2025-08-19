import { NextResponse } from "next/server";
export async function POST(req: Request) {
  const body = await req.json(); // TODO: envoyer sur Discord/Email
  console.log("Contact:", body);
  return NextResponse.json({ ok: true });
}
