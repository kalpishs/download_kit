"""
    Handler progress bar and final cleanup for overall process
"""
from os import path

from tqdm import tqdm

from downloadKit.constants import unit, unit_divisor


class DownloadBuilder(object):
    def __init__(self, url):
        self.url, self.download_processor, self.progress_slider = url, None, None

    def build_progress(self):
        global downloaded, total
        if self.download_processor is not None:
            downloaded, total = self.download_processor.progress()
        else:
            return
        if self.progress_slider is None:
            self.progress_slider = tqdm(
                total=total, desc=path.basename(self.download_processor.file_details),
                unit=unit, unit_scale=True, unit_divisor=unit_divisor, disable=False)
        self.progress_slider.update(downloaded - self.progress_slider.n)


    def clear_incomplete_downloads(self):
        if self.download_processor is not None:
            downloaded, total = self.download_processor.progress()
            if downloaded != total or downloaded == 0:
                self.download_processor.clear()
            return

        pass
