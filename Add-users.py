import argparse
import base64
import csv
import json
import requests

parser = argparse.ArgumentParser()

parser.add_argument("--url", required=True)
parser.add_argument("--pat", required=True)
parser.add_argument("--project", required=True)
parser.add_argument("--group", required=True)
parser.add_argument("--psids", required=True)

args = parser.parse_args()

BASE_URL = args.url.rstrip("/")

token = base64.b64encode(f":{args.pat}".encode()).decode()

HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
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

    r.raise_for_status()

    data = r.json()

    identities = data["results"][0]["identities"]

    if len(identities) == 0:
        return None

    return identities[0]


def get_group(project_name, group_name):

    url = f"{BASE_URL}/_api/_identity/ReadScopedApplicationGroupsJson"

    params = {
        "_v": 5,
        "scope": project_name,
        "readMembers": "false"
    }

    r = requests.get(
        url,
        headers=HEADERS,
        params=params,
        verify=False
    )

    r.raise_for_status()

    data = r.json()

    for g in data["identities"]:

        if g["FriendlyDisplayName"].lower() == group_name.lower():

            return g["TeamFoundationId"]

    return None
