import { NextRequest, NextResponse } from "next/server";
import { supabase } from "@/lib/supabase";

// GET /export/<session_id>  — stream a BlueTally-compatible CSV for the session
export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id: sessionId } = await params;

    // Fetch session metadata
    const { data: session, error: sessionError } = await supabase
      .from("return_sessions")
      .select("*")
      .eq("id", sessionId)
      .single();

    if (sessionError || !session) {
      return NextResponse.json({ error: "Session not found" }, { status: 404 });
    }

    // Fetch items
    const { data: items, error: itemsError } = await supabase
      .from("return_items")
      .select("*")
      .eq("session_id", sessionId)
      .order("created_at", { ascending: true });

    if (itemsError) throw itemsError;

    // Build CSV — BlueTally column order: Name, Asset Tag, Category, Team, Status
    const header = ["Name", "Asset Tag", "Category", "Team", "Status"];
    const rows = (items ?? []).map((item) =>
      [
        csvEscape(item.clean_name || item.raw_name),
        csvEscape(item.asset_tag),
        csvEscape(item.category),
        csvEscape(item.team_name),
        csvEscape(item.status),
      ].join(",")
    );

    const csv = [header.join(","), ...rows].join("\r\n");

    const filename = `returns_${session.event_name.replace(/\s+/g, "_")}_${sessionId.slice(0, 8)}.csv`;

    return new NextResponse(csv, {
      status: 200,
      headers: {
        "Content-Type": "text/csv; charset=utf-8",
        "Content-Disposition": `attachment; filename="${filename}"`,
      },
    });
  } catch (err) {
    console.error("[export]", err);
    return NextResponse.json(
      { error: "Failed to export CSV" },
      { status: 500 }
    );
  }
}

function csvEscape(value: string): string {
  const str = String(value ?? "");
  if (str.includes(",") || str.includes('"') || str.includes("\n")) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}
