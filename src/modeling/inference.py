import requests
import json

def infer(served_model_url, images_array, timeout):
    data = json.dumps({"signature_name": "serving_default", "instances": images_array, "timeout": timeout})
    headers = {"content-type": "application/json"}
    response = requests.post(served_model_url, data=data, headers=headers)
    response.raise_for_status()
    predictions = response.json()["predictions"]

    results_array = predictions

    return results_array

def get_model_meta_data(metadata_url):
    response = requests.get(metadata_url).json()
    return response