import os
from urllib import parse

import pytest

from downloadKit.protocol_factory.ftp import ftpUrlDownloader
from tests.contansts import *


@pytest.mark.parametrize('parse_url, expected', [
    (parse.urlparse(test_ftp_url), test_ftp_url_file_name),
    (parse.urlparse(test_ftp_url_1_file_name), test_ftp_url_1_file_name)])
def test_file_name_engine(parse_url, expected, tmpdir):
    assert ftpUrlDownloader(parse_url, str(tmpdir)).get_file() == expected

def test_ftp_fail_download(mocker, tmpdir):
    ftp_test_url = parse.urlparse(test_ftp_url_1)
    download_kit = ftpUrlDownloader(ftp_test_url, str(tmpdir))
    mocker.patch(ftp_module_path).side_effect = lambda: download_kit.clear()
    download_kit.execute()
    assert not os.path.exists(download_kit.file_details)

def test_ftp_download(mocker, tmpdir):
    ftp_test_url = parse.urlparse(test_ftp_url)
    download_kit = ftpUrlDownloader(ftp_test_url, str(tmpdir))
    mocker.patch(ftp_module_path).side_effect = lambda: open(
        os.path.join(str(tmpdir), test_ftp_url_file_name), 'wb')
    download_kit.execute()
    assert os.path.exists(download_kit.file_details)

