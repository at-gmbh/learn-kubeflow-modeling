import pandas as pd
import numpy as np
from PIL import Image
from modeling import utils, artifact_storage
import boto3
import click
import json

def prepare_data(
        dataset_index_uri: str,
        inputs_uri: str,
        targets_uri: str,
        input_size_x: int,
        input_size_y: int,
        channels: int,
        labels: str,
        base: float = 255.,
        uri_column: str = "uri"
):
    labels=json.loads(labels)

    # read dataset_index from S3
    print(f"Now fetching dataset_index_df from {dataset_index_uri}")
    dataset_index_df = pd.read_csv(dataset_index_uri)

    # initialise empty numpy arrays
    inputs_array = np.zeros((len(dataset_index_df), input_size_x, input_size_y, channels))
    targets_array = np.zeros((len(dataset_index_df), len(labels)))

    # loop through each record in the dataset_index, fetch the image listed there, preprocess it and add it to
    s3 = boto3.Session().resource("s3")
    i=0
    print("Now fetching images")
    for index, row in dataset_index_df.iterrows():

        # read image from s3
        bucket, key = utils.get_bucket_and_key(row[uri_column])
        response = s3.Bucket(bucket).Object(key).get()
        file_stream = response["Body"]
        img = Image.open(file_stream).resize(size=(input_size_x, input_size_y))

        # convert image input numpy array and add to inputs_array
        ar = np.array(img)
        ar = ar / (255./base)
        inputs_array[i] = np.reshape(ar, (input_size_x, input_size_y, channels))

        # added targets to targets_array
        targets_array[i] = row[labels].values

        i=i+1


    #write prepared arrays to s3
    print(f"Now writing inputs with shape {inputs_array.shape} to {inputs_uri}")
    artifact_storage.write_array_to_s3(inputs_uri, inputs_array)

    print(f"Now writing targets with shape {inputs_array.shape} to {targets_uri}")
    artifact_storage.write_array_to_s3(targets_uri, targets_array)


@click.command()
@click.option("--dataset_index_uri")
@click.option("--inputs_uri")
@click.option("--targets_uri")
@click.option("--input_size_x", type=int)
@click.option("--input_size_y", type=int)
@click.option("--channels", type=int)
@click.option("--labels")
@click.option("--base", type=float)
@click.option("--uri_column")
def cli(*args, **kwargs):
    return prepare_data(*args, **kwargs)

if __name__=="__main__":
    cli()
