data = r.json()
groups = data.get("identities", [])

print(f"Total Groups : {len(groups)}")

for g in groups:
    friendly = g.get("FriendlyDisplayName", "")
    display = g.get("DisplayName", "")
    identity_type = g.get("IdentityType", "")

    print(f"{identity_type} -> {friendly}")

    if identity_type not in ("group", "team"):
        continue

    if (
        friendly.lower() == group_name.lower()
        or display.lower().endswith("\\" + group_name.lower())
    ):
        print("\nGroup Found")
        print(friendly)
        return {
            "name": friendly,
            "tfid": g["TeamFoundationId"]
        }

print("Group not found.")
return None
