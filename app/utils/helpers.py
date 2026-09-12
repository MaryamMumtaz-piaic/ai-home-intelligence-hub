def count_furniture(home: dict) -> int:
    return sum(len(r.get("furniture") or []) for r in (home.get("rooms") or []))


def count_appliances(home: dict) -> int:
    return sum(len(r.get("appliances") or []) for r in (home.get("rooms") or []))
