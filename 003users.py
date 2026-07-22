def search_user(psid):

    print(f"\nSearching user : {psid}")

    url = f"{BASE_URL}/_apis/IdentityPicker/Identities"

    payload = {
        "query": psid,
        "identityTypes": [
            "user",
            "group"
        ],
        "operationScopes": [
            "ims",
            "ad",
            "vmd"
        ],
        "options": {
            "MinResults": 10,
            "MaxResults": 10
        }
    }

    r = invoke(
        "POST",
        url,
        json=payload
    )

    if r.status_code != 200:
        return None

    data = r.json()

    if not data.get("results"):
        return None

    identities = data["results"][0].get("identities", [])

    if not identities:
        return None

    user = identities[0]

    print("User :", user["displayName"])

    return {
        "name": user["displayName"],
        "tfid": user["teamFoundationId"]
    }
