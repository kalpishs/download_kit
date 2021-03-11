from urllib import parse
from downloadKit.protocol_factory.constants import chunksize
from downloadKit.protocol_factory.protocol_template import ProtocolTemplate
import os
import logging
import requests


class HttpUrlDownloader(ProtocolTemplate):
    def __init__(self, url, output_dir):
        super().__init__(url, output_dir)
        self._file_length = 0
        self._downloaded_length = 0
        self._req = None
        self._chunk_size = chunksize

    def get_file(self):
        return os.path.basename(self.url.path)

    """
        Main execution of url downloader request
    """

    def execute(self):
        try:
            super().execute()
            self._req = requests.get(parse.urlunparse(self.url), stream=True)
            try:
                self._req.raise_for_status()
                self._file_length = int(self._req.headers['content-length'])
            except KeyError or ValueError:
                print("downloading with missing content length")
            with open(self.file_details, "wb") as file:
                for chunk in self._req.iter_content(chunk_size=self._chunk_size):
                    self._downloaded_length += len(chunk)
                    file.write(chunk)
            self._req.close()
        except Exception as ex:
            print(f"downloading failed {ex}")
            self.clear()

    def clear(self):
        try:
            self.clear_downloads()
            self._req.close()
        except Exception as e:
            logging.info(f"failed closing & clear downloads exception{e}")

    def progress(self):
        return self._downloaded_length, self._file_length
