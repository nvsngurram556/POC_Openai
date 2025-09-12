import msal
import requests
import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the existing config file
config.read('config.ini')

# Access variables
vtenant_id = config['auth']['tenant_id']
vclient_id = config['auth']['client_id']
vclient_secret = config['auth']['client_secret']

# Azure AD app registration info
TENANT_ID = vtenant_id
CLIENT_ID = vclient_id
CLIENT_SECRET = vclient_secret

# SharePoint site info
SHAREPOINT_SITE_DOMAIN = 'thinkspecial.sharepoint.com'  # e.g., contoso.sharepoint.com
SHAREPOINT_SITE_NAME = 'POC'  # e.g., 'marketing'
DOCUMENT_LIBRARY_NAME = 'Documents'  # Usually 'Documents' or 'Shared Documents'

# OAuth2 authority and scope
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ['https://graph.microsoft.com/.default']

def get_access_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=SCOPE)
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception(f"Failed to get access token: {result.get('error_description')}")

def get_site_id(access_token):
    url = f"https://graph.microsoft.com/v1.0/sites/{SHAREPOINT_SITE_DOMAIN}:/sites/{SHAREPOINT_SITE_NAME}"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    site = response.json()
    return site['id']

def get_lists(access_token, site_id):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    lists = response.json()['value']
    return lists

def get_list_items(access_token, site_id, list_id):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_id}/items?expand=fields"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json()['value']
    return items


def get_drive_id(access_token, site_id):
    url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives"
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    drives = response.json()['value']
    for drive in drives:
        if drive['name'] == DOCUMENT_LIBRARY_NAME:
            return drive['id']
    raise Exception(f"Drive '{DOCUMENT_LIBRARY_NAME}' not found")

def list_files(access_token, drive_id, folder_path=None):
    headers = {'Authorization': f'Bearer {access_token}'}
    if folder_path:
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{folder_path}:/children"
    else:
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json()['value']
    for item in items:
        item_type = 'Folder' if 'folder' in item else 'File'
        print(f"{item_type}: {item['name']}")
    return items


if __name__ == "__main__":
    token = get_access_token()
    site_id = get_site_id(token)
    print(f"Site ID: {site_id}")

    lists = get_lists(token, site_id)
    print("Lists in the site:")
    for lst in lists:
        print(f"- {lst['displayName']} (ID: {lst['id']})")

    # Example: Read items from the first list
    if lists:
        first_list_id = lists[0]['id']
        items = get_list_items(token, site_id, first_list_id)
        print(f"\nItems in list '{lists[0]['displayName']}':")
        for item in items:
            print(item['fields'])  # Fields contain the actual list item data

