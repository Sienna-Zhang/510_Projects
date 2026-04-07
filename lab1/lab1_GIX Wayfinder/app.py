from typing import Any, Dict, List, Set

import streamlit as st


# ---------------------------------------------------------------------------
# Data: static list of GIX campus resources stored as Python dicts
# ---------------------------------------------------------------------------

CAMPUS_RESOURCES: List[Dict[str, Any]] = [
    {
        "name": "Makerspace",
        "category": "Lab",
        "location": "GIX Building - 1st Floor",
        "description": "Open workspace with 3D printers, laser cutters, hand tools, and electronics stations for rapid prototyping.",
        "hours": "Mon–Fri 8:00 AM – 10:00 PM, Sat 10:00 AM – 6:00 PM",
        "contact": "makerspace@gix.uw.edu",
        "tags": ["3d printing", "laser cutting", "prototyping", "tools", "fabrication"],
    },
    {
        "name": "Prototyping Lab",
        "category": "Lab",
        "location": "GIX Building - 1st Floor",
        "description": "Dedicated lab space for building and testing physical prototypes, equipped with soldering stations and oscilloscopes.",
        "hours": "Mon–Fri 9:00 AM – 9:00 PM",
        "contact": "protolab@gix.uw.edu",
        "tags": ["soldering", "electronics", "hardware", "testing", "prototype"],
    },
    {
        "name": "PCB Lab",
        "category": "Lab",
        "location": "GIX Building - 1st Floor",
        "description": "Specialized lab for PCB design, etching, and assembly. Includes reflow oven and pick-and-place equipment.",
        "hours": "Mon–Fri 9:00 AM – 6:00 PM",
        "contact": "pcblab@gix.uw.edu",
        "tags": ["pcb", "circuit board", "electronics", "smd", "reflow", "etching"],
    },
    {
        "name": "Student Lounge",
        "category": "Study Space",
        "location": "GIX Building - 2nd Floor",
        "description": "Comfortable lounge area with sofas, whiteboards, and power outlets. Great for informal meetings and relaxation.",
        "hours": "Mon–Sun 7:00 AM – 11:00 PM",
        "contact": "facilities@gix.uw.edu",
        "tags": ["lounge", "relax", "social", "meeting", "whiteboard"],
    },
    {
        "name": "Library",
        "category": "Study Space",
        "location": "GIX Building - 2nd Floor",
        "description": "Quiet study area with reference materials, individual desks, and group study rooms available for reservation.",
        "hours": "Mon–Fri 8:00 AM – 10:00 PM, Sat–Sun 10:00 AM – 8:00 PM",
        "contact": "library@gix.uw.edu",
        "tags": ["books", "study", "quiet", "research", "reading", "group room"],
    },
    {
        "name": "Conference Rooms",
        "category": "Study Space",
        "location": "GIX Building - 2nd Floor",
        "description": "Bookable conference rooms with displays, video conferencing equipment, and whiteboards for team meetings.",
        "hours": "Mon–Fri 8:00 AM – 9:00 PM",
        "contact": "rooms@gix.uw.edu",
        "tags": ["meeting", "conference", "presentation", "video call", "booking"],
    },
    {
        "name": "Staff Office",
        "category": "Office",
        "location": "GIX Building - 3rd Floor",
        "description": "Administrative and faculty offices. Visit for academic advising, program questions, or faculty office hours.",
        "hours": "Mon–Fri 9:00 AM – 5:00 PM",
        "contact": "staff@gix.uw.edu",
        "tags": ["admin", "faculty", "advising", "office hours", "administration"],
    },
    {
        "name": "IT Help Desk",
        "category": "Service",
        "location": "GIX Building - 1st Floor",
        "description": "Technical support for campus Wi-Fi, software licenses, printing issues, and account management.",
        "hours": "Mon–Fri 8:00 AM – 6:00 PM",
        "contact": "ithelp@gix.uw.edu",
        "tags": ["wifi", "network", "software", "tech support", "computer", "account"],
    },
    {
        "name": "Career Services",
        "category": "Service",
        "location": "GIX Building - 3rd Floor",
        "description": "Career counseling, resume reviews, mock interviews, and job/internship placement assistance.",
        "hours": "Mon–Fri 9:00 AM – 5:00 PM",
        "contact": "careers@gix.uw.edu",
        "tags": ["career", "jobs", "internship", "resume", "interview", "employment"],
    },
    {
        "name": "Phone Booth",
        "category": "Service",
        "location": "GIX Building - 2nd Floor",
        "description": "Soundproof phone booths for private calls, virtual meetings, or focused solo work.",
        "hours": "Mon–Sun 7:00 AM – 11:00 PM",
        "contact": "facilities@gix.uw.edu",
        "tags": ["phone", "call", "private", "quiet", "meeting", "booth"],
    },
    {
        "name": "Kitchen",
        "category": "Dining",
        "location": "GIX Building - 2nd Floor",
        "description": "Shared kitchen with microwave, refrigerator, coffee maker, and basic utensils. Please clean up after use.",
        "hours": "Mon–Sun 7:00 AM – 10:00 PM",
        "contact": "facilities@gix.uw.edu",
        "tags": ["food", "microwave", "coffee", "refrigerator", "cook", "lunch"],
    },
    {
        "name": "Vending Machine",
        "category": "Dining",
        "location": "GIX Building - 1st Floor",
        "description": "Snack and beverage vending machines accepting cash, card, and mobile payment.",
        "hours": "24/7",
        "contact": "facilities@gix.uw.edu",
        "tags": ["snacks", "drinks", "beverage", "vending", "food"],
    },
    {
        "name": "Print Station",
        "category": "Service",
        "location": "GIX Building - 1st Floor",
        "description": "Color and black-and-white printing, scanning, and copying. Supports UW Husky Card payment.",
        "hours": "Mon–Fri 8:00 AM – 9:00 PM",
        "contact": "ithelp@gix.uw.edu",
        "tags": ["print", "scan", "copy", "paper", "poster"],
    },
]

# When a keyword matches but filters yield no rows, suggest nearby categories for new students.
RELATED_KEYWORD_HINTS: List[Dict[str, Any]] = [
    {
        "triggers": [
            "coffee",
            "food",
            "eat",
            "snack",
            "drink",
            "lunch",
            "meal",
            "kitchen",
            "hungry",
            "beverage",
            "vending",
        ],
        "categories": ["Dining"],
        "title": "Food & drink nearby",
        "caption": "No exact match with your filters — you might be looking for these dining spots:",
    },
    {
        "triggers": ["wifi", "network", "internet", "print", "computer", "account"],
        "categories": ["Service"],
        "title": "IT & campus services",
        "caption": "Try these service locations:",
    },
    {
        "triggers": ["lab", "prototype", "pcb", "solder", "3d", "laser"],
        "categories": ["Lab"],
        "title": "Labs & making",
        "caption": "These labs might be what you need:",
    },
    {
        "triggers": ["study", "book", "quiet", "meeting", "room"],
        "categories": ["Study Space"],
        "title": "Study & meeting spaces",
        "caption": "Consider these spaces:",
    },
]

# Maps each category to a colored badge for display
CATEGORY_COLORS: Dict[str, str] = {
    "Lab": "#FF6B6B",
    "Study Space": "#4ECDC4",
    "Office": "#45B7D1",
    "Service": "#96CEB4",
    "Dining": "#FFEAA7",
}

_REQUIRED_RESOURCE_KEYS = frozenset(
    {"name", "category", "location", "description", "hours", "contact", "tags"}
)
assert (
    all(_REQUIRED_RESOURCE_KEYS <= r.keys() for r in CAMPUS_RESOURCES)
    and all(isinstance(r["tags"], list) for r in CAMPUS_RESOURCES)
    and all(r["category"] in CATEGORY_COLORS for r in CAMPUS_RESOURCES)
), "Each campus resource must include required keys, list-typed tags, and a category key in CATEGORY_COLORS."


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_all_categories(resources: List[Dict[str, Any]]) -> List[str]:
    """Return a sorted list of unique categories from the resource list."""
    return sorted({r["category"] for r in resources})


def get_all_locations(resources: List[Dict[str, Any]]) -> List[str]:
    """Return a sorted list of unique locations from the resource list."""
    return sorted({r["location"] for r in resources})


def matches_search(resource: Dict[str, Any], query: str) -> bool:
    """Check whether *query* appears (case-insensitive) in name, description, or tags."""
    q = query.lower()
    if q in resource["name"].lower():
        return True
    if q in resource["description"].lower():
        return True
    if any(q in tag.lower() for tag in resource["tags"]):
        return True
    return False


def filter_resources(
    resources: List[Dict[str, Any]],
    search_query: str,
    category: str,
    location: str,
) -> List[Dict[str, Any]]:
    """Apply all active filters (AND logic) and return matched resources sorted by name."""
    results = resources

    if category != "All":
        results = [r for r in results if r["category"] == category]

    if location != "All":
        results = [r for r in results if r["location"] == location]

    if search_query.strip():
        results = [r for r in results if matches_search(r, search_query.strip())]

    return sorted(results, key=lambda r: r["name"])


def render_badge(text: str, color: str) -> str:
    """Return an HTML span styled as a colored badge."""
    return (
        f'<span style="background-color:{color};color:#222;padding:2px 10px;'
        f'border-radius:12px;font-size:0.85em;font-weight:600;">{text}</span>'
    )


# Substring match: used to decide if a keyword should trigger category suggestions.
def hint_triggers_match(query_lower: str, triggers: List[str]) -> bool:
    """Return True if *query_lower* contains any trigger substring."""
    return any(t in query_lower for t in triggers)


# Return which RELATED_KEYWORD_HINTS apply to the user's search string.
def collect_related_hints(search_query: str) -> List[Dict[str, Any]]:
    """Return hint dicts whose triggers match the search text (case-insensitive)."""
    q = search_query.lower().strip()
    if not q:
        return []
    return [h for h in RELATED_KEYWORD_HINTS if hint_triggers_match(q, h["triggers"])]


# Filter resources by category set and sort by name (used for "you might try" suggestions).
def resources_for_categories(
    resources: List[Dict[str, Any]],
    categories: Set[str],
) -> List[Dict[str, Any]]:
    """Return resources whose category is in *categories*, sorted by name."""
    out = [r for r in resources if r["category"] in categories]
    return sorted(out, key=lambda r: r["name"])


# Draw the standard expander list for one or more resources (main results or suggestions).
def render_resource_expanders(resources: List[Dict[str, Any]]) -> None:
    """Render *resources* as expander cards with category badge and details."""
    for resource in resources:
        cat_color = CATEGORY_COLORS.get(resource["category"], "#d3d3d3")
        header = f"{resource['name']}  {render_badge(resource['category'], cat_color)}"

        with st.expander(resource["name"], expanded=False):
            st.markdown(header, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**📍 Location:** {resource['location']}")
                st.markdown(f"**🕐 Hours:** {resource['hours']}")
            with col2:
                st.markdown(f"**📧 Contact:** {resource['contact']}")
            st.markdown("---")
            st.markdown(resource["description"])


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------


def main() -> None:
    """Entry point: renders the full Streamlit app."""
    st.set_page_config(page_title="GIX Campus Wayfinder", page_icon="🗺️", layout="wide")

    st.title("🗺️ GIX Campus Wayfinder")
    st.caption("Find rooms, labs, services, and more across the GIX campus.")

    # ---- Sidebar filters ----
    with st.sidebar:
        st.header("Search & Filter")

        search_query = st.text_input("🔍 Keyword search", placeholder="e.g. prototyping, coffee, wifi …")

        all_categories = ["All"] + get_all_categories(CAMPUS_RESOURCES)
        selected_category = st.selectbox("📂 Category", all_categories)

        all_locations = ["All"] + get_all_locations(CAMPUS_RESOURCES)
        selected_location = st.selectbox("📍 Location", all_locations)

        if st.button("Clear all filters"):
            st.query_params.clear()
            st.rerun()

    # ---- Apply filters ----
    results = filter_resources(CAMPUS_RESOURCES, search_query, selected_category, selected_location)

    # ---- Active-filter summary badges ----
    active_filters: List[str] = []
    if search_query.strip():
        active_filters.append(render_badge(f'Keyword: "{search_query.strip()}"', "#d3d3d3"))
    if selected_category != "All":
        color = CATEGORY_COLORS.get(selected_category, "#d3d3d3")
        active_filters.append(render_badge(f"Category: {selected_category}", color))
    if selected_location != "All":
        active_filters.append(render_badge(f"Location: {selected_location}", "#c8e6c9"))

    if active_filters:
        st.markdown("**Active filters:**  " + "  ".join(active_filters), unsafe_allow_html=True)

    # ---- Results count ----
    st.markdown(f"**Found {len(results)} resource{'s' if len(results) != 1 else ''}**")

    # ---- Resource cards ----
    if results:
        render_resource_expanders(results)
    else:
        st.info(
            "No resources match your current filters. "
            "Try broadening your search or clearing some filters using the sidebar."
        )

        # Related suggestions when keyword matches common intents (e.g. coffee → Dining)
        hints = collect_related_hints(search_query)
        seen_names: Set[str] = {r["name"] for r in results}
        for hint in hints:
            cat_set = set(hint["categories"])
            suggested = resources_for_categories(CAMPUS_RESOURCES, cat_set)
            suggested = [r for r in suggested if r["name"] not in seen_names]
            if not suggested:
                continue
            st.divider()
            st.subheader(f"💡 {hint['title']}")
            st.caption(hint["caption"])
            render_resource_expanders(suggested)
            for r in suggested:
                seen_names.add(r["name"])


if __name__ == "__main__":
    main()
