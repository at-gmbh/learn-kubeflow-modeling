from modeling import artifact_storage
from tensorflow.keras.models import load_model
import os
import click

def predict(
    model_uri: str,
    inputs_uri: str,
    predictions_uri: str,
    temp_dir: str ="./tmp",
):
    # fetch model from s3
    print(f"Now loading model from {model_uri}")
    temp_path=os.path.join(temp_dir, os.path.split(model_uri)[1])
    artifact_storage.copy_from_s3_to_disk(
        source_uri=model_uri,
        target_path=temp_path
    )

    # load model
    model= load_model(temp_path)

    # read inputs from S3
    print("Now loading input data from {inputs_uri}")
    inputs_array = artifact_storage.read_array_from_s3(inputs_uri)

    # predict
    print("Now predicting")
    predictions = model.predict(inputs_array)

    # save predictions to S3
    print("Now storing prediction to {predictions_uri}")
    artifact_storage.write_array_to_s3(predictions_uri, predictions)

@click.command()
@click.option("--model_uri")
@click.option("--inputs_uri")
@click.option("--predictions_uri")
@click.option("--temp_dir")
def cli(*args, **kwargs):
    return predict(*args, **kwargs)

if __name__=="__main__":
    cli()