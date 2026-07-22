import json
import requests

def can_add_member(group_id, user_local_id):
    url = f"{BASE_URL}/_api/_identity/CanAddMemberToGroup"

    params = {
        "_v": 5,
        "groupId": group_id,
        "memberId": user_local_id
    }

    r = requests.get(
        url,
        headers=HEADERS,
        params=params,
        verify=False
    )

    print("CanAddMemberToGroup:", r.status_code)

    if r.status_code != 200:
        print(r.text)
        return False

    return True


def add_identity(group_id, user_local_id):

    url = f"{BASE_URL}/_api/_identity/AddIdentities?_v=5"

    payload = {
        "existingUsersJson": json.dumps([user_local_id]),
        "groupsToJoinJson": json.dumps([group_id]),
        "newUsersJson": "[]",
        "aadGroupsJson": "[]"
    }

    r = requests.post(
        url,
        headers=HEADERS,
        data=payload,
        verify=False
    )

    print("AddIdentities:", r.status_code)
    print(r.text)

    return r.status_code == 200
