from azure.storage.blob import BlobServiceClient,BlobClient
import os
from dotenv import load_dotenv

load_dotenv()

#Azure Blob credentials
Azure_Blob_Connection_String = os.getenv("AZURE_BLOB_CONNECTION_STR")
Azure_Blob_Container_Name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(Azure_Blob_Connection_String)

# Create a ContainerClient using blob service client
container_client = blob_service_client.get_container_client(Azure_Blob_Container_Name)

#List all blobs in the container
print("\nListing blobs...")

# List the blobs in the container
blob_list = container_client.list_blobs()
for blob in blob_list:
    print("\t" + blob.name)