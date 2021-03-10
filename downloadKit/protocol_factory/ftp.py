import logging
import os
from abc import ABC
from urllib import parse

from downloadKit.protocol_factory.constants import blocksize
from downloadKit.protocol_factory.protocol_template import ProtocolTemplate
from ftplib import FTP

class ftpUrlDownloader(ProtocolTemplate):
    def __init__(self, url, output_dir):
        super().__init__(url, output_dir)
        self._file_length = 0
        self._downloaded_length = 0
        self._ftp = FTP()

    def get_file(self):
        return os.path.basename(self.url.path)

    """
    execution of url downloader request for ftp
    """
    def execute(self):
        try:
            dir_name = os.path.dirname(self.url.path)
            super().execute()
            try:
                self._ftp.connect(host=self.url.hostname, port=self.url.port or 0)
                self._ftp.login(self.url.username, self.url.password)
            except:
                logging.info(f"login error Url: {parse.urlunparse(self.url)}")
                print(f"ftp login error for {parse.urlunparse(self.url)}")
                self.clear()
            server_filename = os.path.basename(self.url.path)
            if dir_name:
                self._ftp.cwd(dir_name)
            self._file_length = self._ftp.size(self.url.path)
            with open(self.file_details, 'wb') as f:
                def callback(data):
                    self._downloaded_length += len(data)
                    f.write(data)
                self._ftp.retrbinary('RETR %s' % server_filename, callback,blocksize)
        except Exception as e:
            print(e)
            self.clear()
            pass

    def clear(self):
        try:
            self.clear_downloads()
            if self._ftp.sock is not None:
                self._ftp.abort()
        except Exception as e:
            logging.info(f"failed closing & clearing downloads exception{e}")
            print("failed closing & clearing downloads.")

    def progress(self):
        return self._downloaded_length, self._file_length
