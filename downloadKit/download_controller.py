import os
import queue
import logging
import sys
import time
from threading import Thread
from downloadKit import constants
from downloadKit import download_builder
from tqdm import tqdm
from urllib import parse

# Controller entry point for all Urls list to be processed in multi-threads for parallelization
from downloadKit.decision_engine import DecisionEngine


class DownloadController(object):
    """instanceate the DownloadController object and initialize queue for downloading urls async way"""
    def __init__(self, **kwargs):
        self._download_url_list = []
        self.output_dir = kwargs.get('output_dir')
        self._urls = queue.Queue()
        self._download_urls_list = kwargs.get('downloadUrls')

        for indx, download_urls in enumerate(self._download_urls_list):
            self._download_url_list.insert(indx, download_builder.DownloadBuilder(download_urls))
            self._urls.put((indx, download_urls))

    def garbage_handler(self):
        logging.info(f"Clearing unsuccessfully downloads in {self.output_dir} ")
        for urls_list in self._download_url_list:
            urls_list.clear_incomplete_downloads()

    def execute(self):
        """
            Creates a processor thread workers based on urls passed.
        """
        logging.info("initiating treads for DownloadController")
        try:
            life_cycle_hook = Thread(target=self.life_cycle_hook)
            life_cycle_hook.start()

            for i in range(constants.thread_pool_size):
                t = Thread(target=self.download_processor)
                t.start()
            self._urls.join()
            life_cycle_hook.join()
            self.garbage_handler()

        except KeyboardInterrupt:
            tqdm.write('Download Interrupted Failure!!')
            self.garbage_handler()
            sys.exit("Keyboard Interrupt - Cancel downloading tasks")
            pass
        finally:
            logging.info("exiting thread")

    def life_cycle_hook(self):
        try:
            while self._urls.unfinished_tasks > 0:
                self.update_process_bar()
                time.sleep(1)
            self.update_process_bar()
            time.sleep(1)
            self.garbage_handler()
            logging.info(f"Successfully downloaded in {self.output_dir}")
            tqdm.write('Process Complete')
        except:
            tqdm.write('Download failure!!')
            self.garbage_handler()
            sys.exit("exiting downloading tasks")
            pass
        pass

    def download_processor(self):
        while True:
            try:
                indx, download_url = self._urls.get_nowait()
            except Exception:
                logging.info(f"Nothing to process in the download queue")
                break
            parsed_url = parse.urlparse(download_url)
            """download with proper protocol and update the process"""
            download_execution = self.process_url(parsed_url)
            if download_execution is not None:
                self._download_url_list[indx].download_processor = download_execution
                download_execution.execute()
            self._urls.task_done()
        pass

    def process_url(self, parsed_url):
        try:
            output_dir = os.path.join(self.output_dir)
            download_process = DecisionEngine().get_protocol(parsed_url)(parsed_url, output_dir)
            return download_process
        except NotImplementedError as e:
            logging.info(f"implementation of {parsed_url.scheme} unavailable")
            print(f'error: {e} skipping: {parse.urlunparse(parsed_url)}')
            return

    def update_process_bar(self):
        for update_process_bars in self._download_url_list:
            update_process_bars.build_progress()