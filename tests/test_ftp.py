import os
from urllib import parse

import pytest

from downloadKit.protocol_factory.ftp import ftpUrlDownloader
from tests.contansts import *


@pytest.mark.parametrize('parse_url, expected', [
    (parse.urlparse(test_ftp_url), test_ftp_url_file_name),
    (parse.urlparse(test_ftp_url_1_file_name), test_ftp_url_1_file_name)])
def test_decision_engine(parse_url, expected, tmpdir):
    assert ftpUrlDownloader(parse_url, str(tmpdir)).get_file() == expected

def test_ftp_fail(mocker, tmpdir):
    ftp_test_url = parse.urlparse(test_ftp_url_1)
    downloader = ftpUrlDownloader(ftp_test_url, str(tmpdir))
    mocker.patch(ftp_module_path).side_effect = lambda: downloader.clear()
    downloader.execute()
    assert not os.path.exists(downloader.file_details)

def test_ftp_pass(mocker, tmpdir):
    ftp_test_url = parse.urlparse('ftp://example.net/ftp_test.zip')
    downloader = ftpUrlDownloader(ftp_test_url, str(tmpdir))
    mocker.patch(ftp_module_path).side_effect = lambda: open(
        os.path.join(str(tmpdir), 'ftp_test.zip'), 'wb')
    downloader.execute()
    assert os.path.exists(downloader.file_details)

