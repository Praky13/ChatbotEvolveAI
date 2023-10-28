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


local_path = "D:\PrakashFiles\EvolveAI\Docs"

for files in os.listdir(local_path):

        #pdf blob name and json file path
        pdf_blob_name = ''.join(os.path.splitext(os.path.basename(files)))

        blob_name=pdf_blob_name
        blob_client = BlobClient.from_connection_string(Azure_Blob_Connection_String, container_name=Azure_Blob_Container_Name,blob_name=pdf_blob_name)
        # Upload the JSON file to Azure Blob Storage
        try:
            
            with open("Docs/"+files, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            print(f'Upload succeeded: {blob_name}')

        except Exception as ex:
            print(f'Upload failed1: {blob_name}')
            print(ex)

       
print("Files uploaded to Azure Blob Storage.")

