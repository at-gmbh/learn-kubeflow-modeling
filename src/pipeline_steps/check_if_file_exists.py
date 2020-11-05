from s3fs.core import S3FileSystem
import click


def check_if_file_exits(uri: str) -> bool:

    print("Now checking if file exists at {}".format(uri))

    s3_filesystem = S3FileSystem(anon=False)
    exists = s3_filesystem.exists(uri)

    print(exists)

    return exists

@click.command()
@click.option("--uri")
def cli(*args, **kwargs) -> bool:
    return check_if_file_exits(*args, **kwargs)

if __name__=="__main__":
    cli()
