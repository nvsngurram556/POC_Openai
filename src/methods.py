from msal import ConfidentialClientApplication
import msal
import requests
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the existing config file
config.read('config.ini')

# Azure AD app registration info
TENANT_ID = config['auth']['tenant_id']
CLIENT_ID = config['auth']['client_id']
CLIENT_SECRET = config['auth']['client_secret']

# SharePoint site info
SHAREPOINT_SITE_DOMAIN = config['auth']['sharepoint_site']  # e.g., contoso.sharepoint.com
SHAREPOINT_SITE_NAME = config['auth']['sharepoint_site_name']  # e.g., 'marketing'
DOCUMENT_LIBRARY_NAME = config['auth']['sharepoint_library_name']  # Usually 'Documents' or 'Shared Documents'

# You can get site-id via the Graph API; see function below
GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_BASE = "https://graph.microsoft.com/v1.0"

def get_access_token():
    app = ConfidentialClientApplication(
        CLIENT_ID, authority=f"https://login.microsoftonline.com/{TENANT_ID}",
        client_credential=CLIENT_SECRET
    )
    resp = app.acquire_token_for_client(scopes=GRAPH_SCOPE)
    if "access_token" not in resp:
        raise Exception(f"Token error: {resp}")
    return resp["access_token"]

def get_site_id_by_path(hostname, site_relative_path):
    # hostname e.g. "contoso.sharepoint.com"
    token = get_access_token()
    url = f"{GRAPH_BASE}/sites/{hostname}:/sites/{site_relative_path}"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()["id"]  # site-id

def get_list_id(site_id, list_name):
    token = get_access_token()
    url = f"{GRAPH_BASE}/sites/{site_id}/lists"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    for lst in r.json().get("value", []):
        if lst.get("displayName") == list_name:
            return lst["id"]
    raise Exception("List not found")

def update_list_item_fields(site_id, list_id, item_id, fields_payload):
    token = get_access_token()
    url = f"{GRAPH_BASE}/sites/{site_id}/lists/{list_id}/items/{item_id}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    r = requests.patch(url, headers=headers, json=fields_payload)
    r.raise_for_status()
    return r.json()
