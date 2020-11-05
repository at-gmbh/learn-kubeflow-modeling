from modeling import inference, artifact_storage
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import json

import click

def predict_from_endpoint(
    model_inference_url: str,
    model_metadata_url: str,
    inputs_uri: str,
    endpoint_predictions_uri: str,
    batch_size: int = 8,
    timeout: int = 60,
):

    # fetch metadata:
    print(f"Now fetching model metadata from {model_metadata_url}")
    response = inference.get_model_meta_data(model_metadata_url)
    print(json.dumps(response, indent=2))

    # read inputs from S3
    print(f"Now loading input data from {inputs_uri}")
    inputs_array = artifact_storage.read_array_from_s3(inputs_uri)

    # predict

    generator=ImageDataGenerator().flow(inputs_array, batch_size=int(batch_size))

    inferences=[]
    print(f"> Now requesting predictions from {model_inference_url}")
    for i in range(len(generator)):
        batch=next(generator)
        print(f"> Now requesting predictions on batch with shape: {batch.shape}")
        inferences.append(inference.infer(model_inference_url, batch.tolist(), timeout))

    inferences=np.array(inferences)

    # save predictions to S3
    print(f"Now storing prediction to {endpoint_predictions_uri}")
    artifact_storage.write_array_to_s3(endpoint_predictions_uri, inferences)

@click.command()
@click.option("--model_inference_url")
@click.option("--model_metadata_url")
@click.option("--inputs_uri")
@click.option("--endpoint_predictions_uri")
@click.option("--batch_size")
@click.option("--timeout")
def cli(*args, **kwargs):
    return predict_from_endpoint(*args, **kwargs)

if __name__=="__main__":
    cli()