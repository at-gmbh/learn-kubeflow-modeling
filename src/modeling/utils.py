import logging
from pathlib import Path
from typing import Any, Dict, Union
import yaml
from urllib.parse import urlparse
import mlflow

logger = logging.getLogger('utils')

def get_bucket_and_key(s3_uri):
    parsed = urlparse(s3_uri)
    return parsed.netloc, parsed.path[1:]


def load_config(config_file: Union[str, Path]) -> Dict[str, Any]:
    with open(config_file, 'r') as fp:
        return yaml.safe_load(fp)

