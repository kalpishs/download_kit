from unittest import TestCase

import pytest
from downloadKit.decision_engine import DecisionEngine
from urllib import parse

from downloadKit.protocol_factory.ftp import ftpUrlDownloader
from downloadKit.protocol_factory.http import HttpUrlDownloader
from downloadKit.protocol_factory.sftp import sftpUrlDownloader
from tests.contansts import *


@pytest.mark.parametrize('parse_url, expected', [
    (parse.urlparse(test_ftp_url_1), ftpUrlDownloader),
    (parse.urlparse(test_http_url1), HttpUrlDownloader),
    (parse.urlparse(test_sftp_url_1), sftpUrlDownloader),
])
def test_decision_engine(parse_url, expected):
    return_downloader = DecisionEngine.get_protocol(parse_url)
    assert return_downloader == expected

def test_unsupported_protocol():
    parsed_url = parse.urlparse('newscheme://unknownfake.path')
    with pytest.raises(NotImplementedError):
        DecisionEngine.get_protocol(parsed_url)