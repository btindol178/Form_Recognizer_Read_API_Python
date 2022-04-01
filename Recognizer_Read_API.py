# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 08:05:13 2022

@author: btindol
"""

"""
This code sample shows Prebuilt Read operations with the Azure Form Recognizer client library. 
The async versions of the samples require Python 3.6 or later.

To learn more, please visit the documentation - Quickstart: Form Recognizer Python client library SDKs v3.0
https://docs.microsoft.com/en-us/azure/applied-ai-services/form-recognizer/quickstarts/try-v3-python-sdk
"""
#pip install azure-ai-formrecognizer==3.2.0b3 # beta version get  DocumentAnalysisClient problem cant find function in library
# pip install azure
#pip install azure-core
from azure.core.credentials import AzureKeyCredential
#pip install azure-ai-formrecognizer
#pip install azure-storage-blob==0.37.1 
# pip install azure-storage-blob
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
# pip install azure-storage-blob --upgrade

#connect_str = os.getenv('Connection_String') # retrieve the connection string from the environment variable
connect_str = "<Connection_String>" # retrieve the connection string from the environment variable

container_name = "<Conainer_Name" # container name in which images will be store in the storage account

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str) # create a blob service client to interact with the storage account

container_client = blob_service_client.get_container_client(container=container_name)

endpoint = "https://<Location Example EastUS>.api.cognitive.microsoft.com/"
key = "Secret Key"

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

def analyze_read():
   
    # go into the url in the blob where you want to find your uploaded pdf
    #formUrl = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"
    formUrl = "https://<Storage Account Name>.blob.core.windows.net/<Container>/<Folder>/<File.png>"
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    poller = document_analysis_client.begin_analyze_document_from_url(
            "prebuilt-read", formUrl)
    result = poller.result()

    print ("Document contains content: ", result.content)
    
    # # Writing the results to a text file for later analysis send this to the blob!! 
    samplename = "sample.txt"
    text_file = open(samplename, "w")
    n = text_file.write(result.content)
    text_file.close()

    for idx, style in enumerate(result.styles):
        print(
            "Document contains {} content".format(
                "handwritten" if style.is_handwritten else "no handwritten"
            )
        )

    for page in result.pages:
        print("----Analyzing Read from page #{}----".format(page.page_number))
        print(
            "Page has width: {} and height: {}, measured with unit: {}".format(
                page.width, page.height, page.unit
            )
        )

        for line_idx, line in enumerate(page.lines):
            print(
                "...Line # {} has text content '{}' within bounding box '{}'".format(
                    line_idx,
                    line.content,
                    format_bounding_box(line.bounding_box),
                )
            )

        for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )

    print("----------------------------------------")



if __name__ == "__main__":
    analyze_read()
