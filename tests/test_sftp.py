import os
from urllib import parse

import pytest

from downloadKit.protocol_factory.sftp import sftpUrlDownloader
from tests.contansts import *


@pytest.mark.parametrize('parse_url, expected', [
    (parse.urlparse(test_sftp_url_1), test_sftp_url_1_name),
    (parse.urlparse(test_sftp_url_with_port), test_sftp_url_with_port_name)])
def test_decision_engine(parse_url, expected, tmpdir):
    assert sftpUrlDownloader(parse_url, str(tmpdir)).get_file() == expected

def test_sftp_failed_download(mocker, tmpdir):
    ftp_test_url = parse.urlparse(test_sftp_url_1)
    download_kit = sftpUrlDownloader(ftp_test_url, str(tmpdir))
    mocker.patch(sftp_module_path).side_effect = lambda: download_kit.clear()
    download_kit.execute()
    assert not os.path.exists(download_kit.file_details)

def test_sftp_download(mocker, tmpdir):
    ftp_test_url = parse.urlparse(test_sftp_url_with_port)
    download_kit = sftpUrlDownloader(ftp_test_url, str(tmpdir))
    mocker.patch(sftp_module_path).side_effect = lambda: open(os.path.join(str(tmpdir), test_sftp_url_with_port_name), 'wb')
    download_kit.execute()
    assert os.path.exists(download_kit.file_details)
