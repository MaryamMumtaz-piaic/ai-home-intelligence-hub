"""Pure-Python validation of a home profile dict — no OpenAI calls.

Checks for missing/incomplete information that would limit how useful the AI
analysis can be, and produces a rough data-completeness percentage so the
orchestrator and UI can be transparent with the user about how much of the
report is based on solid data versus assumptions.
"""

from typing import Any


def _room_completeness(room: dict) -> tuple[list[str], int, int]:
    """Return (missing_notes, filled_count, total_checked) for a single room."""
    missing: list[str] = []
    checks = 0
    filled = 0

    name = room.get("name")
    checks += 1
    if name:
        filled += 1

    room_type = room.get("room_type")
    checks += 1
    if room_type:
        filled += 1
    else:
        missing.append(f"Room '{name or room.get('id', 'unknown')}' is missing a room type.")

    length_m = room.get("length_m")
    width_m = room.get("width_m")
    checks += 1
    if length_m and width_m:
        filled += 1
    else:
        missing.append(
            f"Room '{name or room.get('id', 'unknown')}' is missing dimensions "
            "(length/width), which limits space-planning suggestions."
        )

    checks += 1
    if room.get("primary_purpose"):
        filled += 1
    else:
        missing.append(
            f"Room '{name or room.get('id', 'unknown')}' has no stated primary purpose."
        )

    checks += 1
    furniture = room.get("furniture") or []
    if furniture:
        filled += 1
    else:
        missing.append(
            f"Room '{name or room.get('id', 'unknown')}' has no furniture listed."
        )

    return missing, filled, checks


def validate_home(home: dict) -> dict:
    """Inspect a HomeProfile-shaped dict and report missing information plus
    an overall data-completeness percentage (0-100).

    Never raises - always returns a valid dict, even for an empty/malformed
    home input.
    """
    if not isinstance(home, dict):
        return {
            "missing_information": ["No home information is available yet."],
            "data_completeness_percent": 0,
        }

    missing: list[str] = []
    total_checks = 0
    total_filled = 0

    def check(condition: bool, note: str) -> None:
        nonlocal total_checks, total_filled
        total_checks += 1
        if condition:
            total_filled += 1
        else:
            missing.append(note)

    check(bool(home.get("name")), "The home has no name set.")
    check(bool(home.get("home_type")), "The home type has not been specified.")
    check(
        bool(home.get("approximate_total_area_sqm")),
        "Approximate total home area is not provided, which limits space and energy insights.",
    )
    check(
        bool(home.get("climate_zone_or_location")),
        "Climate zone or location is not provided, which limits energy and comfort insights.",
    )
    check(
        bool(home.get("resident_count")),
        "Number of residents is not provided.",
    )
    check(
        bool(home.get("main_goals")),
        "No main goals have been selected, so recommendations may be less targeted.",
    )

    rooms: list[dict[str, Any]] = home.get("rooms") or []
    check(bool(rooms), "No rooms have been added yet.")

    if not rooms:
        missing.append(
            "Add at least one room with dimensions and furniture to get a meaningful analysis."
        )
    else:
        for room in rooms:
            if not isinstance(room, dict):
                continue
            room_missing, filled, checks = _room_completeness(room)
            missing.extend(room_missing)
            total_checks += checks
            total_filled += filled

    lifestyle = home.get("lifestyle") or {}
    check(
        bool(lifestyle.get("top_priority")),
        "No top lifestyle priority has been set.",
    )

    energy = home.get("energy") or {}
    check(
        bool(energy.get("approximate_monthly_bill") or energy.get("typical_monthly_consumption_kwh")),
        "No energy usage information (monthly bill or consumption) has been provided, "
        "which limits energy insights.",
    )
    check(
        bool(energy.get("main_cooling_method") or energy.get("main_heating_method")),
        "Cooling/heating method information is not provided.",
    )

    security = home.get("security") or {}
    check(
        "smoke_alarms" in security,
        "Safety equipment information (smoke alarms, etc.) is incomplete.",
    )

    if total_checks == 0:
        percent = 0
    else:
        percent = round((total_filled / total_checks) * 100)
        percent = max(0, min(100, percent))

    return {
        "missing_information": missing,
        "data_completeness_percent": percent,
    }
