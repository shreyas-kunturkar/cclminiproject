from flask import Flask, render_template,request
import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
subs_key="b0d38fb402fe4eab8f392767ed03b5e6"

endpoint="https://eastus.api.cognitive.microsoft.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subs_key))


app=Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html',text="")


@app.route("/image_to_text",methods=["GET","POST"])
def image_to_text():
    if request.method=="POST":
        image_data=request.form.get("files")
        read_response = computervision_client.read(image_data,  raw=True,model_version="2022-01-30-preview")
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]
        while True:
            read_result = computervision_client.get_read_result(operation_id)
            if read_result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        img_text=''
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    img_text+=line.text+'\n'
                    # print(line.text)
                    # print(line.bounding_box)
        return render_template('index.html',text=img_text)
    else:
        return redirect('/')


if __name__=="__main__":
    app.run(host='0.0.0.0')
