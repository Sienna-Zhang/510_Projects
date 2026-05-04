# Component A: Staff Interview — Maason Kao

## Interview Notes

**Interviewee:** Maason Kao  
**Role:** IT Staff, GIX — manages equipment checkout and return  
**Context:** Post-Launch event (end-of-year demo), when all student teams must return purchased/borrowed equipment

---

### Current Workflow Summary

After the Launch poster session and demos, every team must return all purchased items to Maason and Kevin (IT/Makerspace staff). The process unfolds as follows:

1. Maason and Kevin set up a return table on the 3rd floor
2. Teams arrive with their items
3. Staff check each item off a **manual return list**, one by one
4. First, any items checked out via **BlueTally** (GIX's inventory software) are verified and checked back in
5. Then, purchased items (which have no existing barcode) are physically inspected
6. Maason and Kevin decide whether each item belongs in **IT** (Maason), **Makerspace** (Kevin), or is consumed/discarded
7. Pre-generated **UW asset tag stickers** (8-digit barcodes) are physically applied to items
8. Items are manually added to **BlueTally** one by one, or via CSV upload

### Systems Involved

| System | Description |
|--------|-------------|
| **BlueTally** | Inventory management software. Tracks all checkout-able assets. Has CSV import and a student-facing portal (GIX Hub). API endpoints exist but require a paid plan. |
| **Purchase/procurement system** | Workflow through which teams buy items (separate from BlueTally; no barcode assigned at purchase time) |
| **Manual return list** | Spreadsheet or printout listing everything each team checked out/purchased — used during the return table session |
| **Microsoft Power Automate** | A script (written by Alan) pulls overdue items from BlueTally and sends automated email reminders to students |
| **GIX Hub (student portal)** | A website where students can log in to view available assets; they can technically request checkouts but are expected to come in person |

### Pain Points

1. **Slow one-by-one check-in:** Going through every item on the list manually with each team is time-consuming, especially during a high-volume return event.
2. **Double data entry — purchase vs. return:** Items are tracked when purchased (procurement system) and again when returned to BlueTally, with no automated bridge between the two.
3. **No barcode until return day:** Items purchased for prototypes don't receive a UW asset tag until the return session, meaning staff can't pre-populate BlueTally ahead of time.
4. **Messy Amazon-style product names:** Purchase records contain long Amazon titles (e.g., *"hollyland Lark m2 wireless microphone for iPhone 15 16 17 Android"*). These need to be cleaned into simple names before import into BlueTally.
5. **CSV import friction:** BlueTally supports CSV upload, but Maason has struggled to use it for annual returns — primarily because of the product name normalization issue above.
6. **Small items are hard to tag:** Items too small for a sticker (e.g., earbuds, cables) either get labeled on the box (which gets thrown away) or are tracked as generic interchangeable accessories with no unique barcode.
7. **Verification gaps:** Items are sometimes reported returned but cannot be found later. Cameras are especially problematic due to multiple components inside a single case.
8. **Paid API barrier:** BlueTally's API endpoints (which would allow automation) are behind a paid plan that GIX is not currently using.

---

## System Map Sketch

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        EQUIPMENT RETURN SYSTEM                              │
└─────────────────────────────────────────────────────────────────────────────┘

 [STUDENT TEAM]
      │  Brings items to return table
      │  (physical hand-off)
      ▼
 ┌──────────────────────────────────┐
 │   RETURN TABLE (3rd floor)       │  ← TOUCHPOINT 1
 │   Maason + Kevin (staff)         │
 │   Manual return checklist        │
 └────────────┬─────────────────────┘
              │
    ┌─────────┴──────────┐
    │                    │
    ▼                    ▼
 [Checked-out         [Purchased items
  items from           (no barcode yet)]
  BlueTally]                │
    │                       │ Apply UW asset
    │ Check in via           │ tag sticker
    │ BlueTally              │
    │                       ▼
    │              ┌──────────────────┐
    │              │  Categorize item  │
    │              │  IT / Makerspace /│  ← PAIN POINT: manual decision
    │              │  Discard          │
    │              └───────┬──────────┘
    │                      │
    └──────────────────────┤
                           ▼
              ┌────────────────────────┐
              │       BLUETALLY        │
              │  (Inventory software)  │
              │                        │
              │  Option A: Manual      │  ← PAIN POINT: slow, one-by-one
              │  entry via web UI      │
              │                        │
              │  Option B: CSV upload  │  ← PAIN POINT: product name
              │  (batch import)        │    normalization fails
              └────────────┬───────────┘
                           │
             ┌─────────────┘
             │
             ▼
   ┌─────────────────────┐
   │  POWER AUTOMATE     │
   │  (Alan's script)    │──────────────────────► [STUDENT EMAIL]
   │  Overdue reminders  │                          (automated nudge)
   └─────────────────────┘

   ┌─────────────────────┐
   │  GIX HUB (portal)   │◄─────────────────────── [STUDENT LOGIN]
   │  View available     │                          browse assets
   │  assets             │
   └─────────────────────┘

   ┌─────────────────────┐
   │  PROCUREMENT SYSTEM │
   │  (purchase records) │───── no automated link ──►  BlueTally
   │  Amazon-style names │                              (manual bridge)
   └─────────────────────┘

⚠️  Pain Points (circled):
    ① Manual one-by-one return check (slow, error-prone)
    ② No barcode at purchase time → double work at return
    ③ Product name normalization before CSV import
    ④ Verification gaps (items go missing, camera parts)
    ⑤ Paid API blocks automation
```

---

## System Touchpoints

### Touchpoint 1: Return Table Check-In

| Annotation | Detail |
|------------|--------|
| **Who** | Two people simultaneously: (1) **IT/Makerspace staff** (Maason or Kevin) running the checklist, and (2) **Student team members** handing back items |
| **What they are doing** | Staff verbally calls out each item on the return list; student confirms they have it and physically hands it over; staff marks it off the list and checks it into BlueTally |
| **What device** | Staff: **desktop or laptop** at the return table (logging into BlueTally web UI); Student: no device — purely physical hand-off in person |

> **Design signal:** This is the highest-friction touchpoint. The interaction requires staff attention on two things at once (the physical item and the screen), with a queue of teams waiting. Any app supporting this moment must be extremely fast to operate and ideally scannable (barcode input) rather than relying on typed text. The interface needs to work well on a **desktop** at a fixed station.

---

### Touchpoint 2: Overdue Item Email Notification

| Annotation | Detail |
|------------|--------|
| **Who** | **Student** who has not yet returned a checked-out item |
| **What they are doing** | Receiving an automated email reminder; reading the message and deciding whether to go return the item |
| **What device** | **Mobile phone** (most likely — students receive email on the go, between classes or in transit) |

> **Design signal:** This notification reaches students in a mobile context. If there were a self-service return status page or a return scheduling feature, it would need to be **mobile-friendly** — readable on a narrow screen, with a single clear call-to-action button rather than a complex table.

---

## Build Mandate

> "Based on the interview, I will build a **return check-in assistant that scans/reads asset tags and normalizes product names for BlueTally CSV upload** because Maason said *'the friction point is the product name — can we break down this item description that's been stuffed into the title so that it can get hidden on Amazon, into an actual product name'* and *'it takes quite some time to go through each item one by one,'* which means the design decision it drives is to **prioritize batch processing over individual item entry, with automated name cleaning as a core feature rather than an afterthought.**"
