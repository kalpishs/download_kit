"""Test get_file function"""
import os
import pytest

from downloadKit.protocol_factory.http import HttpUrlDownloader
from tests.contansts import *
from tests.http_mock_handler import HttpMockHandler
from urllib import parse


class TestHttpUrlDownloader(object):
    @pytest.fixture(autouse=True)
    def start_mock_server(self):
        self.mocked_port=HttpMockHandler.get_port()
        HttpMockHandler.mocked_server(self.mocked_port)

    def test_execute_http_downloading(self, tmpdir, monkeypatch):
        fake_parse_url= parse.urlparse(http_protocol +"://" + str(host) +":" + str(self.mocked_port) +'/' + str(http_url1_file_name))
        http_url_downloader_obj=HttpUrlDownloader(fake_parse_url,str(tmpdir))
        monkeypatch.setattr(http_url_downloader_obj, 'url', fake_parse_url)
        http_url_downloader_obj.execute()
        assert (os.path.exists(http_url_downloader_obj.file_details)) and open(http_url_downloader_obj.file_details).readline() == content.decode('utf-8')


    def test_execute_http_failed_downloading(self, tmpdir, monkeypatch):
        fake_parse_url= parse.urlparse(http_protocol+"://"+str(host)+":"+str(self.mocked_port)+'/test_none.txt')
        http_url_downloader_obj = HttpUrlDownloader(fake_parse_url, str(tmpdir))
        monkeypatch.setattr(http_url_downloader_obj, 'url', fake_parse_url)
        http_url_downloader_obj.execute()
        assert not (os.path.exists(http_url_downloader_obj.file_details))
        pass

    pass



@pytest.mark.parametrize('parse_url, expected', [
    (parse.urlparse(test_http_url), http_url_file_name),
    (parse.urlparse(test_https_url1), https_url1_file_name)
])
def test_decision_engine(parse_url, expected, tmpdir):
    assert HttpUrlDownloader(parse_url, str(tmpdir)).get_file() == expected

