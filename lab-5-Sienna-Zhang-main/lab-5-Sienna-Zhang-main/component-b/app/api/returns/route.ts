import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

// GET /api/returns?session_id=<uuid>  — list items in a session
export async function GET(req: NextRequest) {
  try {
    const sessionId = req.nextUrl.searchParams.get("session_id");
    if (!sessionId) {
      return NextResponse.json(
        { error: "session_id is required" },
        { status: 400 }
      );
    }

    const { data, error } = await supabase
      .from("return_items")
      .select("*")
      .eq("session_id", sessionId)
      .order("created_at", { ascending: true });

    if (error) throw error;
    return NextResponse.json({ items: data });
  } catch (err) {
    console.error("[returns GET]", err);
    return NextResponse.json(
      { error: "Failed to fetch return items" },
      { status: 500 }
    );
  }
}

// POST /api/returns  — create a new return item
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const { session_id, team_name, raw_name, clean_name, asset_tag, category } =
      body;

    if (!session_id || !team_name || !raw_name || !category) {
      return NextResponse.json(
        { error: "session_id, team_name, raw_name, category are required" },
        { status: 400 }
      );
    }

    const validCategories = ["IT", "Makerspace", "Discard"];
    if (!validCategories.includes(category)) {
      return NextResponse.json(
        { error: `category must be one of: ${validCategories.join(", ")}` },
        { status: 400 }
      );
    }

    const { data, error } = await supabase
      .from("return_items")
      .insert({
        session_id,
        team_name,
        raw_name,
        clean_name: clean_name ?? "",
        asset_tag: asset_tag ?? "",
        category,
        status: "pending",
      })
      .select()
      .single();

    if (error) throw error;
    return NextResponse.json({ item: data }, { status: 201 });
  } catch (err) {
    console.error("[returns POST]", err);
    return NextResponse.json(
      { error: "Failed to create return item" },
      { status: 500 }
    );
  }
}

// PATCH /api/returns  — update item status
export async function PATCH(req: NextRequest) {
  try {
    const body = await req.json();
    const { id, status } = body;

    if (!id || !status) {
      return NextResponse.json(
        { error: "id and status are required" },
        { status: 400 }
      );
    }

    const validStatuses = ["pending", "returned", "missing"];
    if (!validStatuses.includes(status)) {
      return NextResponse.json(
        { error: `status must be one of: ${validStatuses.join(", ")}` },
        { status: 400 }
      );
    }

    const { data, error } = await supabase
      .from("return_items")
      .update({ status })
      .eq("id", id)
      .select()
      .single();

    if (error) throw error;
    return NextResponse.json({ item: data });
  } catch (err) {
    console.error("[returns PATCH]", err);
    return NextResponse.json(
      { error: "Failed to update return item" },
      { status: 500 }
    );
  }
}
