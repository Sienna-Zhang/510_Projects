import { NextRequest, NextResponse } from "next/server";
import Anthropic from "@anthropic-ai/sdk";

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const rawName: string = body.raw_name;

    if (!rawName || typeof rawName !== "string" || rawName.trim() === "") {
      return NextResponse.json(
        { error: "raw_name is required" },
        { status: 400 }
      );
    }

    const message = await anthropic.messages.create({
      model: "claude-haiku-4-5",
      max_tokens: 60,
      messages: [
        {
          role: "user",
          content: `You are an asset name cleaner. Given a raw Amazon product name, return a short, clean asset name in Title Case. Keep the brand, model number, and key descriptor. Remove filler words, marketing language, and excessive detail. Reply with ONLY the clean name — no explanation, no punctuation at the end.\n\nRaw name: ${rawName}`,
        },
      ],
    });

    const cleanName =
      message.content[0]?.type === "text"
        ? message.content[0].text.trim()
        : rawName;

    return NextResponse.json({ clean_name: cleanName });
  } catch (err) {
    console.error("[normalize]", err);
    return NextResponse.json(
      { error: "Failed to normalize name" },
      { status: 500 }
    );
  }
}
