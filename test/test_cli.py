import pathlib

import pytest

import omforme.cli as cli

TEST_PREFIX = pathlib.Path('test', 'fixtures')
DEFAULT_DOCUMENTS_PATH = TEST_PREFIX
TEST_MAKE_MISSING = 'missing-this-file-for-'


def test_parse_request(capsys):
    options = cli.parse_request([])
    assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert 'usage: omforme [-h] [--quiet] [--verbose]' in out
    assert not err


def test_parse_request_pos_doc_root_not_present(capsys):
    with pytest.raises(SystemExit) as err:
        cli.parse_request([f'{TEST_MAKE_MISSING}{DEFAULT_DOCUMENTS_PATH}', '-q', '-v'])
    assert err.value.code == 2
    out, err = capsys.readouterr()
    assert not out
    message_part = f'omforme: error: unrecognized arguments: {TEST_MAKE_MISSING}{DEFAULT_DOCUMENTS_PATH}'
    assert message_part in err
