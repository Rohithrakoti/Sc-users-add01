import argparse
import base64
import json
import csv
import requests
import urllib3

urllib3.disable_warnings()

parser = argparse.ArgumentParser(description="Add users to Azure DevOps Project Group")

parser.add_argument("--url", required=True)
parser.add_argument("--pat", required=True)
parser.add_argument("--project", required=True)
parser.add_argument("--group", required=True)
parser.add_argument("--psids", required=True)

args = parser.parse_args()

BASE_URL = args.url.rstrip("/")

pat_token = base64.b64encode(f":{args.pat}".encode()).decode()

HEADERS = {
    "Authorization": f"Basic {pat_token}",
    "User-Agent": "Mozilla/5.0"
}


def search_user(psid):

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
        "filterByAncestorEntityIds": [],
        "filterByEntityIds": [],
        "options": {
            "MinResults": 40,
            "MaxResults": 40
        },
        "properties": [
            "DisplayName",
            "ScopeName",
            "SamAccountName",
            "Active",
            "SubjectDescriptor",
            "Department"
        ]
    }

    r = requests.post(
        url,
        headers=HEADERS,
        json=payload,
        verify=False
    )

    print("IdentityPicker:", r.status_code)

    if r.status_code != 200:
        print(r.text)
        return None

    data = r.json()

    if "results" not in data:
        return None

    if len(data["results"]) == 0:
        return None

    identities = data["results"][0].get("identities", [])

    if len(identities) == 0:
        return None

    return identities[0]


def get_group(project_name, group_name):

    url = f"{BASE_URL}/_api/_identity/ReadScopedApplicationGroupsJson"

    params = {
        "_v": 5
    }

    r = requests.get(
        url,
        headers=HEADERS,
        params=params,
        verify=False
    )

    print("Groups:", r.status_code)

    if r.status_code != 200:
        print(r.text)
        return None

    data = r.json()

    groups = data.get("identities", [])

    for group in groups:

        display = group.get("FriendlyDisplayName", "")

        if display.lower() == group_name.lower():

            print("Found Group:", display)

            return group.get("TeamFoundationId")

    return None
