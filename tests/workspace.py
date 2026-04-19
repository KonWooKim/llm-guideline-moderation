from __future__ import annotations

import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path

from test_support import REPO_ROOT


TEST_TMP_ROOT = REPO_ROOT / ".tmp_test_runs"


@contextmanager
def workspace_tmpdir():
    TEST_TMP_ROOT.mkdir(exist_ok=True)
    path = TEST_TMP_ROOT / str(uuid.uuid4())
    path.mkdir(parents=True, exist_ok=False)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)
