from abc import ABC, abstractmethod
import os
import logging
from downloadKit.constants import max_duplicate_files


class ProtocolTemplate(ABC):
    def __init__(self, url, output_dir):
        self.url = url
        self._op_dir = output_dir
        self._op_file = None
        self._error = None

    @property
    def file_details(self):
        if self._op_file:
            return self._op_file
        file_name=self.get_file()
        count = 0
        duplicate_file_name=file_name
        if file_name == '':
            raise FileNotFoundError('cannot download due to file unavailable.')
        while True:
            if count >= max_duplicate_files:
                break
            count=count + 1
            download_filepath = os.path.join(self._op_dir, duplicate_file_name)
            if self._create_file(download_filepath):
                return self._op_file
            file_ext = os.path.splitext(file_name)
            duplicate_file_name=file_ext[0]+"_" + str(count) +file_ext[1]
        raise RuntimeError(f'Cannot download due to internal error OR reached max duplicate files allowed i.e: {max_duplicate_files}')


    @abstractmethod
    def get_file(self):
        return ''

    '''
    create a writable file if possible otherwise create dup name
    '''
    def _create_file(self, download_filepath):
        try:
            with open(download_filepath, 'x'):
                self._op_file=download_filepath
        except FileExistsError:
            return None
        else:
            return self.file_details()
        pass

    def clear_downloads(self):
        if self.file_details is not None and os.path.exists(self.file_details):
            print(f"clear un-downloaded file {self.file_details}")
            logging.info(f"clearing downloaded file {self.file_details}")
            os.remove(self.file_details)

    @abstractmethod
    def execute(self):
        try:
            os.makedirs(os.path.dirname(self.file_details))
        except:
            logging.info(f"directory already exist Dir Name:{os.path.dirname(self.file_details)}")

    @abstractmethod
    def progress(self):
        raise NotImplementedError("implement progress")
