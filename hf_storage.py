import json
import os
from huggingface_hub import HfApi, hf_hub_download
from io import BytesIO

REPO_ID = "GIRISHSANKAR/edubot-storage"
REPO_TYPE = "dataset"
HF_TOKEN = os.environ.get("HF_TOKEN")

api = HfApi()

def load_json_from_hf(filename):
    try:
        path = hf_hub_download(
            repo_id=REPO_ID,
            filename=filename,
            repo_type=REPO_TYPE,
            token=HF_TOKEN
        )
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json_to_hf(filename, data):
    try:
        json_bytes = json.dumps(data, indent=2).encode("utf-8")
        api.upload_file(
            path_or_fileobj=BytesIO(json_bytes),
            path_in_repo=filename,
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            token=HF_TOKEN
        )
    except Exception as e:
        print(f"HF save error: {e}")