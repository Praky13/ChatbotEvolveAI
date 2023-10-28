

import os
from azure.storage.blob import BlobServiceClient,BlobClient
from dotenv import load_dotenv

load_dotenv()

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient 
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    CorsOptions,
    SearchIndex,
    ScoringProfile,
    SearchFieldDataType,
    SimpleField,
    SearchableField
)



Azure_Search_Service_Name = os.getenv("AZURE_SEARCH_SERVICE_NAME")
Azure_Search_Admin_Key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
Azure_Search_Index_Name = os.getenv("AZURE_SEARCH_INDEX_NAME")



endpoint = "https://{}.search.windows.net/".format(Azure_Search_Service_Name)
admin_client = SearchIndexClient(endpoint=endpoint,
                      index_name=Azure_Search_Index_Name,
                      credential=AzureKeyCredential(Azure_Search_Admin_Key))

search_client = SearchClient(endpoint=endpoint,
                      index_name=Azure_Search_Index_Name,
                      credential=AzureKeyCredential(Azure_Search_Admin_Key))


try:
    # Create a service client
    client = SearchIndexClient(endpoint, AzureKeyCredential(Azure_Search_Admin_Key))

    # Create the index
    name = "evolveaiindex"
    fields = [
        SimpleField(name="Chapter", type=SearchFieldDataType.String, key=True),  # Specify 'hotelId' as the key field
        SearchableField(name="Description", type=SearchFieldDataType.String),
        SearchableField(name="PageNo", type=SearchFieldDataType.String)
    ]
    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    scoring_profiles = []

    index = SearchIndex(
        name=name,
        fields=fields,
        scoring_profiles=scoring_profiles,
        cors_options=cors_options)

    result = client.create_index(index)
    print("Index Created", result)

except Exception as e:
    print(e)



