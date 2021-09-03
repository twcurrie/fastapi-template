import json
from pathlib import Path

from app import get_version


def test__get_version__no_file(tmpdir):
    assert {} == get_version(tmpdir)


def test__get_version__success(tmpdir, get_resource):
    with get_resource("version.json") as file:
        expected = file.read()
        with Path(tmpdir / "version.json").open("w") as version_file:
            version_file.write(expected)
        expected_dict = json.loads(expected)

    assert expected_dict == get_version(tmpdir)
