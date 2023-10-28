import openai
import os
import streamlit as st
from streamlit_chat import message
from azure.storage.blob import BlobServiceClient,BlobClient

from dotenv import load_dotenv
load_dotenv()

# Access the Openai credentials 
Azure_Openai_Key = os.getenv("AZURE_OPENAI_KEY")
Azure_Openai_Type = os.getenv("AZURE_OPENAI_TYPE")
Azure_Openai_Version = os.getenv("AZURE_OPENAI_VERSION")
Azure_Openai_Engine = os.getenv("AZURE_OPENAI_ENGINE")
Azure_Openai_Endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

# Set OpenAI API configuration
openai.api_key = Azure_Openai_Key
openai.api_type =Azure_Openai_Type
openai.api_base = Azure_Openai_Endpoint
openai.api_version =Azure_Openai_Version
engine=Azure_Openai_Engine


# Read the File through the form recognizer module
Form_Recognizer_Key = os.getenv("FR_KEY")
Form_Recognizer_Endpoint = os.getenv("FR_ENDPOINT")

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

endpoint = Form_Recognizer_Endpoint
key = AzureKeyCredential(Form_Recognizer_Key)


#Azure Blob credentials
Azure_Blob_Connection_String = os.getenv("AZURE_BLOB_CONNECTION_STR")
Azure_Blob_Container_Name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

# Create a BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(Azure_Blob_Connection_String)

# Create a ContainerClient using blob service client
container_client = blob_service_client.get_container_client(Azure_Blob_Container_Name)


def pdf_text(endpoint,key,pdf_path):
    #  Creating the FormRecognizerClient with a token credential.
    form_recognizer_client = FormRecognizerClient(endpoint, key)
    #Read the pdf file in binary mode
    with open("Docs/"+pdf_path, "rb") as pdf_file:
        pdf = pdf_file.read()
    # Extract all the text from pdf file
    # Extract text and content/layout information from a given document.
    poller = form_recognizer_client.begin_recognize_content(pdf)
    result = poller.result()
    #save the results in list
    extracted_text=[]
    for page in result:
        for line in page.lines:
            extracted_text.append(line.text)
    return(("").join(extracted_text))      

local_path = "Docs"

text = ""
#for files in os.listdir(local_path):
#    text+=pdf_text(endpoint,key,files)  


text += pdf_text(endpoint,key,"ITPolicySoftwareNetworking.pdf")
text += pdf_text(endpoint,key,"GEM.pdf") 
text += pdf_text(endpoint,key,"HRPolicy.pdf") 
text += pdf_text(endpoint,key,"SOP-AVU.pdf")



def generate_response(prompt):
       response1 = openai.ChatCompletion.create(
            
                engine = engine,  #openai model deployment name
                #A list of messages comprising the conversation so far.
                messages = [{"role": "system", "content": "You are AI bot who can answer the question from given text."},
                {"role": "user", "content": f"Extract the answer for this question:{prompt} from the text:{text}.\
                Do not generate any redundant or unnecessary information"}
                ],
                max_tokens = 1000,    #maximum tokens model can generate
                temperature = 0,    #For randomness in the result

        )
       message = response1.choices[0]['message']['content']
       return message



st.title("PRPC Chatbot By Evolve AI team")

# Storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
     input_text = st.text_input("You: ","",key="input")
     return input_text

user_input = get_text()

if user_input:
     output = generate_response(user_input)

     # Store the output
     st.session_state.past.append(user_input)
     st.session_state.generated.append(output)    

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
