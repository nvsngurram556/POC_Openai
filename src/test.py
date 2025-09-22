from methods import get_access_token, get_site_id_by_path, get_list_id, update_list_item_fields, SHAREPOINT_SITE_DOMAIN, SHAREPOINT_SITE_NAME, DOCUMENT_LIBRARY_NAME

# Example usage:
if __name__ == "__main__":
    site_id = get_site_id_by_path(SHAREPOINT_SITE_DOMAIN, SHAREPOINT_SITE_NAME)
    list_id = get_list_id(site_id, DOCUMENT_LIBRARY_NAME)
    item_id = 1
    updated = update_list_item_fields(site_id, list_id, item_id, {"Title": "Test_list1", "Skills": "Python, SSIS, DataStage, Supervised Learning, Unsupervised Learning, Llama, RAG", "Status": "New"})
    print("Updated fields:", updated)
