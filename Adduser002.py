def can_add_member(group_id, user_id):

    url = f"{BASE_URL}/_api/_identity/CanAddMemberToGroup"

    params = {
        "_v": 5,
        "groupId": group_id,
        "memberId": user_id
    }

    r = requests.get(
        url,
        headers=HEADERS,
        params=params,
        verify=False
    )

    print(f"CanAddMemberToGroup : {r.status_code}")

    if r.status_code != 200:
        print(r.text)
        return False

    return True


def add_identity(group_id, user_id):

    url = f"{BASE_URL}/_api/_identity/AddIdentities?_v=5"

    payload = {
        "existingUsersJson": json.dumps([user_id]),
        "groupsToJoinJson": json.dumps([group_id]),
        "newUsersJson": "[]",
        "aadGroupsJson": "[]"
    }

    headers = HEADERS.copy()

    headers["Content-Type"] = "application/x-www-form-urlencoded"

    r = requests.post(
        url,
        headers=headers,
        data=payload,
        verify=False
    )

    print(f"AddIdentities : {r.status_code}")
    print(r.text)

    return r.status_code == 200


def write_report(results):

    with open("report.csv", "w", newline="") as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow([
            "PSID",
            "Display Name",
            "Status"
        ])

        writer.writerows(results)

    print("Report generated : report.csv")


def main():

    results = []

    group_id = get_group(args.project, args.group)

    if group_id is None:
        print("Group not found.")
        return

    psid_list = [x.strip() for x in args.psids.split(",")]

    for psid in psid_list:

        print("=" * 60)
        print(f"Processing : {psid}")

        user = search_user(psid)

        if user is None:
            print("User not found")

            results.append([
                psid,
                "",
                "User Not Found"
            ])

            continue

        display_name = user.get("displayName", "")

        user_id = user.get("localId")

        print(f"Display Name : {display_name}")
        print(f"User LocalId : {user_id}")

        if not can_add_member(group_id, user_id):

            results.append([
                psid,
                display_name,
                "Already Member / Cannot Add"
            ])

            continue

        status = add_identity(group_id, user_id)

        if status:

            results.append([
                psid,
                display_name,
                "Added Successfully"
            ])

        else:

            results.append([
                psid,
                display_name,
                "Failed"
            ])

    write_report(results)

    print("\nCompleted Successfully")


if __name__ == "__main__":
    main()
