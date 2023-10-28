from azure.storage.blob import BlobClient
from threading import Thread
import os

from dotenv import load_dotenv

load_dotenv()

Azure_Blob_Connection_String = os.getenv("AZURE_BLOB_CONNECTION_STR")
Azure_Blob_Container_Name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

# Uploads a single blob. May be invoked in thread.
def upload_blob(container, file, index=0, result=None):
    if result is None:
        result = [None]

    try:
        # extract blob name from file path
        blob_name = ''.join(os.path.splitext(os.path.basename(file)))

        blob = BlobClient.from_connection_string(
            conn_str=Azure_Blob_Connection_String,
            container_name=container,
            blob_name=blob_name
        )

        with open(file, "rb") as data:
            blob.upload_blob(data, overwrite=True)

        print(f'Upload succeeded: {blob_name}')
        result[index] = True # example of returning result
    except Exception as e:
        print(e) # do something useful here
        result[index] = False # example of returning result


# container: string of container name. This example assumes the container exists.
# files: list of file paths.    
def upload_wrapper(container, files):
    # here, you can define a better threading/batching strategy than what is written
    # this code just creates a new thread for each file to be uploaded
    parallel_runs = len(files)
    threads = [None] * parallel_runs
    results = [None] * parallel_runs
    for i in range(parallel_runs):
        t = Thread(target=upload_blob, args=(container, files[i], i, results))
        threads[i] = t
        threads[i].start()

    for i in range(parallel_runs):  # wait for all threads to finish
        threads[i].join()

    # do something with results here


local_path = "D:\PrakashFiles\EvolveAI\Docs"

upload_wrapper(Azure_Blob_Container_Name,local_path)