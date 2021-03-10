import logging
import shutil
from urllib import parse

from downloadKit.protocol_factory.constants import bufsize
from downloadKit.protocol_factory.protocol_template import ProtocolTemplate
import paramiko
import os


class sftpUrlDownloader(ProtocolTemplate):
    def __init__(self, url, output_dir):
        super().__init__(url, output_dir)
        self._file_length = 0
        self._downloaded_length = 0
        self._sftp = None

    def get_file(self):
        return os.path.basename(self.url.path)

    """
    execution of url downloader request for sftp
    """

    def execute(self):
        try:
            super().execute()
            try:
                port_binding = paramiko.Transport((self.url.hostname, self.url.port or 0))
                port_binding.connect(username=self.url.username, password=self.url.password)
                self._sftp = paramiko.SFTPClient.from_transport(port_binding)
            except Exception as e:
                logging.info(f"login error Url: {parse.urlunparse(self.url)}")
                print(f"login error Url: {parse.urlunparse(self.url)}")
                print(f"exception as {e}")
            self._file_length=self._sftp.stat(self.url.path).st_size
            with open(self.file_details, 'wb') as f:
                with self._sftp.open(self.url.path, mode="r", bufsize=bufsize) as write_file:
                    self._downloaded_length= self._file_length * 0.10
                    shutil.copyfileobj(write_file, f)
                self._downloaded_length = self._file_length
        except Exception as ex:
            print(f"downloading failed {ex}")
            self.clear()

    def clear(self):
        try:
            self.clear_downloads()
            self._sftp.close()
        except Exception as e:
            logging.info(f"failed closing & clearing downloads exception{e}")
            print("failed closing & clearing downloads.")

    def progress(self):
        return self._downloaded_length, self._file_length
