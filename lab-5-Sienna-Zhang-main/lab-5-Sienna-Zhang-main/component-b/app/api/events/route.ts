import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

const VALID_CATEGORIES = [
  "guest_lecture",
  "workshop",
  "career_panel",
  "other",
] as const;

// GET /api/events?category=<category>  — list events, optional category filter
export async function GET(req: NextRequest) {
  try {
    const category = req.nextUrl.searchParams.get("category");

    if (
      category &&
      !VALID_CATEGORIES.includes(category as (typeof VALID_CATEGORIES)[number])
    ) {
      return NextResponse.json(
        { error: `category must be one of: ${VALID_CATEGORIES.join(", ")}` },
        { status: 400 }
      );
    }

    let query = supabase
      .from("events")
      .select("*")
      .order("event_date", { ascending: true });

    if (category) {
      query = query.eq("category", category);
    }

    const { data, error } = await query;
    if (error) throw error;

    return NextResponse.json({ events: data });
  } catch (err) {
    console.error("[events GET]", err);
    return NextResponse.json(
      { error: "Failed to fetch events" },
      { status: 500 }
    );
  }
}

// POST /api/events  — create a new event
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { title, description, category, event_date, location } = body;

    if (!title || !category || !event_date) {
      return NextResponse.json(
        { error: "title, category, and event_date are required" },
        { status: 400 }
      );
    }

    if (
      !VALID_CATEGORIES.includes(category as (typeof VALID_CATEGORIES)[number])
    ) {
      return NextResponse.json(
        { error: `category must be one of: ${VALID_CATEGORIES.join(", ")}` },
        { status: 400 }
      );
    }

    const { data, error } = await supabase
      .from("events")
      .insert({
        title,
        description: description ?? "",
        category,
        event_date,
        location: location ?? "",
      })
      .select()
      .single();

    if (error) throw error;
    return NextResponse.json({ event: data }, { status: 201 });
  } catch (err) {
    console.error("[events POST]", err);
    return NextResponse.json(
      { error: "Failed to create event" },
      { status: 500 }
    );
  }
}
