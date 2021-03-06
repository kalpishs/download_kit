
from downloadKit.constants import *
from downloadKit.protocol_factory.ftp import ftpUrlDownloader
from downloadKit.protocol_factory.http import HttpUrlDownloader
from downloadKit.protocol_factory.sftp import sftpUrlDownloader

"""
    Protocol factory class to get instance of correct protocol for each url
"""

class DecisionEngine(object):
    @staticmethod
    def get_protocol(parsed_url):
        options = {http_protocol: HttpUrlDownloader, https_protocol: HttpUrlDownloader, ftp_protocol: ftpUrlDownloader,
                   sftp_protocol: sftpUrlDownloader}
        protocol = options.get(parsed_url.scheme, other_protocols)
        if protocol is other_protocols:
            raise NotImplementedError(f'unsupported download type {parsed_url.scheme}')
        else:
            return protocol
