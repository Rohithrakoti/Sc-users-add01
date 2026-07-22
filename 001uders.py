import argparse
import base64
import csv
import json
import os
import sys
import requests
import urllib3

urllib3.disable_warnings()

# -----------------------------
# Command Line Arguments
# -----------------------------
parser = argparse.ArgumentParser(
    description="Add Azure DevOps users to a project group"
)

parser.add_argument("--url", required=True)
parser.add_argument("--pat", required=True)
parser.add_argument("--project", required=True)
parser.add_argument("--group", required=True)
parser.add_argument("--psids", required=True)

args = parser.parse_args()

BASE_URL = args.url.rstrip("/")
PROJECT = args.project
GROUP = args.group
PSIDS = [x.strip() for x in args.psids.split(",") if x.strip()]

# -----------------------------
# Authentication
# -----------------------------
token = base64.b64encode(f":{args.pat}".encode()).decode()

HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json"
}

# -----------------------------
# CSV Report
# -----------------------------
os.makedirs("reports", exist_ok=True)

CSV_FILE = "reports/report.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "PSID",
            "User",
            "Group",
            "Status",
            "Message"
        ])

def write_report(psid, user, group, status, message):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            psid,
            user,
            group,
            status,
            message
        ])
