import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path):
    os.environ["QUEUE_MODE"] = "inline"
    os.environ["STORAGE_ROOT"] = str(tmp_path / "data")
    os.environ["MAX_UPLOAD_SIZE_MB"] = "1"
    os.environ["ALLOWED_EXTENSIONS_CSV"] = ".nii,.nii.gz,.zip"
    os.environ["GENERATE_STUB_PDF"] = "true"

    from app.core.config import get_settings

    get_settings.cache_clear()

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client

    get_settings.cache_clear()
