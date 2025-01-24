from google.cloud import storage
import os

_bucket = None
GCS_BUCKET = os.environ["GCS_BUCKET"]


def get_gcp_bucket() -> storage.Client:
    global _bucket
    if _bucket is None:
        storage_client = storage.Client()
        _bucket = storage_client.bucket(GCS_BUCKET)
    return _bucket
