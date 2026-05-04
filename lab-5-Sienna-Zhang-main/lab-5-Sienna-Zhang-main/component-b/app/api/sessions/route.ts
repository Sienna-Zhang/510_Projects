import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

// GET /api/sessions  — list all sessions newest first
export async function GET() {
  try {
    const { data, error } = await supabase
      .from("return_sessions")
      .select("*")
      .order("created_at", { ascending: false });

    if (error) throw error;
    return NextResponse.json({ sessions: data });
  } catch (err) {
    console.error("[sessions GET]", err);
    return NextResponse.json(
      { error: "Failed to fetch sessions" },
      { status: 500 }
    );
  }
}

// POST /api/sessions  — create a new return session
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { event_name, staff_name } = body;

    if (!event_name || !staff_name) {
      return NextResponse.json(
        { error: "event_name and staff_name are required" },
        { status: 400 }
      );
    }

    const { data, error } = await supabase
      .from("return_sessions")
      .insert({ event_name, staff_name })
      .select()
      .single();

    if (error) throw error;
    return NextResponse.json({ session: data }, { status: 201 });
  } catch (err) {
    console.error("[sessions POST]", err);
    return NextResponse.json(
      { error: "Failed to create session" },
      { status: 500 }
    );
  }
}
