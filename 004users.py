def get_group(project_name, group_name):

    print(f"\nSearching group '{group_name}' in project '{project_name}'")

    # NOTE:
    # Replace PROJECT_SCOPE_GUID with the actual project scope if needed.
    # Later we'll make this dynamic.
    PROJECT_SCOPE_GUID = "187b4a51-2026-4700-bb2d-ca113b4387fd"

    url = f"{BASE_URL}/_api/_identity/ReadScopedApplicationGroupsJson"

    params = {
        "_v": 5,
        "scope": PROJECT_SCOPE_GUID,
        "readMembers": "false"
    }

    r = invoke(
        "GET",
        url,
        params=params
    )

    if r.status_code != 200:
        return None

    data = r.json()

    groups = data.get("identities", [])

    print(f"Total Groups : {len(groups)}")

    for g in groups:

        friendly = g.get("FriendlyDisplayName", "")
        display = g.get("DisplayName", "")

        if friendly.lower() == group_name.lower() or \
           display.lower().endswith("\\" + group_name.lower()):

            print("\nGroup Found")

            print("Friendly Name :", friendly)
            print("Display Name  :", display)
            print("TFID          :", g["TeamFoundationId"])

            return {
                "name": friendly,
                "tfid": g["TeamFoundationId"]
            }

    print("\nGroup not found.\n")

    print("Available Groups:")

    for g in groups:
        print(" -", g.get("FriendlyDisplayName"))

    return None
