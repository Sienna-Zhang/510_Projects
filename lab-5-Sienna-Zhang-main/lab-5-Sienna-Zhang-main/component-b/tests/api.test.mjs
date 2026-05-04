/**
 * Component D — API Contract Tests
 * Component E — Supabase Asserts
 *
 * Run against dev server:  node --test tests/api.test.mjs
 * Run against production:  API_BASE_URL=https://your-app.vercel.app node --test tests/api.test.mjs
 *
 * Requires Node 18+ (built-in fetch + node:test).
 */

import { test, describe } from "node:test";
import assert from "node:assert/strict";

const BASE = process.env.API_BASE_URL ?? "http://localhost:3000";

// ---------------------------------------------------------------------------
// Component D — /api/returns  (3 API contract tests)
// ---------------------------------------------------------------------------

describe("Component D — /api/returns contract", () => {
  /**
   * Test 1 (valid): GET /api/returns with a well-formed session_id
   *   → 200 + { items: [] }  (empty array is valid for a session with no items)
   *
   * NOTE: This test requires the Supabase `return_items` table to exist.
   * Run supabase/schema.sql in the Supabase SQL Editor if the table is missing.
   */
  test("valid GET with session_id returns 200 and items array", async () => {
    // Use a valid UUID that may not exist; the API must still return 200 + empty array
    const res = await fetch(
      `${BASE}/api/returns?session_id=00000000-0000-0000-0000-000000000000`
    );

    // If 500, the Supabase table likely does not exist — schema.sql must be run first.
    assert.equal(
      res.status,
      200,
      `status should be 200. Got ${res.status} — check that return_items table exists in Supabase`
    );

    const json = await res.json();
    assert.ok(
      Object.prototype.hasOwnProperty.call(json, "items"),
      'response should have "items" key'
    );
    assert.ok(Array.isArray(json.items), "items should be an array");
  });

  /**
   * Test 2 (invalid input): GET /api/returns without session_id
   *   → 400 + { error: "..." }  containing the word "session_id"
   */
  test("GET without session_id returns 400 with descriptive error", async () => {
    const res = await fetch(`${BASE}/api/returns`);

    assert.equal(res.status, 400, "status should be 400");

    const json = await res.json();
    assert.ok(json.error, 'response should have non-empty "error" field');
    assert.match(
      json.error,
      /session_id/i,
      'error message should mention "session_id"'
    );
  });

  /**
   * Test 3 (invalid payload): POST /api/returns with an invalid category
   *   → 400 + { error: "..." }  containing the word "category"
   */
  test("POST with invalid category returns 400 with descriptive error", async () => {
    const res = await fetch(`${BASE}/api/returns`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: "00000000-0000-0000-0000-000000000000",
        team_name: "Test Team",
        raw_name: "Test Item Name",
        category: "DOES_NOT_EXIST",
      }),
    });

    assert.equal(res.status, 400, "status should be 400");

    const json = await res.json();
    assert.ok(json.error, 'response should have non-empty "error" field');
    assert.match(
      json.error,
      /category/i,
      'error message should mention "category"'
    );
  });
});

// ---------------------------------------------------------------------------
// Component E — /api/events  Supabase asserts (2 asserts)
// ---------------------------------------------------------------------------

describe("Component E — /api/events Supabase asserts", () => {
  /**
   * Assert 1: GET /api/events (no filter)
   *   → 200 + { events: Array }
   *   Each event in the array must have the correct Supabase schema shape.
   *
   * NOTE: Requires the Supabase `events` table to exist (run supabase/schema.sql first).
   */
  test("GET /api/events returns 200 with events array matching Supabase schema", async () => {
    const res = await fetch(`${BASE}/api/events`);

    assert.equal(
      res.status,
      200,
      `status should be 200. Got ${res.status} — check that the events table exists in Supabase`
    );

    const json = await res.json();
    assert.ok(
      Object.prototype.hasOwnProperty.call(json, "events"),
      'response must have "events" key'
    );
    assert.ok(Array.isArray(json.events), "events must be an array");

    // If Supabase returned any rows, verify the shape of the first row
    if (json.events.length > 0) {
      const evt = json.events[0];

      assert.ok(typeof evt.id === "string", "event.id must be a string (uuid)");
      assert.ok(
        typeof evt.title === "string" && evt.title.length > 0,
        "event.title must be a non-empty string"
      );
      assert.ok(
        ["guest_lecture", "workshop", "career_panel", "other"].includes(
          evt.category
        ),
        `event.category must be a valid enum value, got: ${evt.category}`
      );
      assert.ok(
        typeof evt.event_date === "string",
        "event.event_date must be a string (date)"
      );
    }
  });

  /**
   * Assert 2: GET /api/events?category=<invalid>
   *   → 400 + { error: "..." }  (Supabase query never reached; validation rejects it)
   */
  test("GET /api/events with invalid category returns 400 (Supabase guard)", async () => {
    const res = await fetch(`${BASE}/api/events?category=definitely_not_valid`);

    assert.equal(
      res.status,
      400,
      "invalid category should be rejected before hitting Supabase"
    );

    const json = await res.json();
    assert.ok(json.error, 'response must have non-empty "error" field');
    assert.match(
      json.error,
      /category/i,
      'error message should reference "category"'
    );
  });
});
