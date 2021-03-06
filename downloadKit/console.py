import os
from os import path
import sys
import argparse
import tempfile
import shutil
import atexit
from downloadKit import download_controller

'''
Function to parse input argument for input file having URLS & output directory. 
'''
def argument_parser():

    parsObj = argparse.ArgumentParser()

    ldir = tempfile.mkdtemp()
    atexit.register(lambda dir=ldir: shutil.rmtree(ldir))
    #File containing URLs to download from.
    parsObj.add_argument('-i', '--inputFile', type=argparse.FileType('r', encoding='UTF-8'), default=sys.stdin,
                        help='File containing urls (default: stdin)')

    #Output directory of downloaded files.
    parsObj.add_argument('-o', '--output_dir', action=writeable_dir, default=ldir,
                        help='Output directory path')
    args = parsObj.parse_args()
    return args


class writeable_dir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir=values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a valid path".format(prospective_dir))
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace,self.dest,prospective_dir)
        else:
            raise argparse.ArgumentTypeError("readable_dir:{0} is not a readable dir".format(prospective_dir))


def main():
    print("enter here")
    args = argument_parser()
    downloadUrls = [urls.strip() for urls in args.inputFile.readlines()]
    output_dir = args.output_dir
    controller = download_controller.DownloadController(output_dir=output_dir,downloadUrls=downloadUrls)
    controller.execute()

