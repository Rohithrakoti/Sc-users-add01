results = []

group_id = get_group(args.project, args.group)

if not group_id:
    print("Group not found")
    exit(1)

for psid in args.psids.split(","):

    psid = psid.strip()

    user = search_user(psid)

    if user is None:
        results.append([psid, "User Not Found"])
        continue

    user_local_id = user["localId"]

    if not can_add_member(group_id, user_local_id):
        results.append([psid, "Cannot Add"])
        continue

    if add_identity(group_id, user_local_id):
        results.append([psid, "Added"])
    else:
        results.append([psid, "Failed"])
