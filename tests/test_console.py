import argparse

from downloadKit.console import argument_parser, main
from tests.contansts import sys_arg

from tests.fixture import *

def test_argument_parser(monkeypatch,in_file, tmpdir):
    monkeypatch.setattr(
        sys_arg,
        ['download_kit',
         '-i', in_file,
         '-o', str(tmpdir)])
    args = argument_parser()
    assert args.inputFile.name == in_file
    assert args.output_dir == str(tmpdir)


def test_argument_parser_invalid_param(monkeypatch, in_file, tmpdir):
    args = [
        ['download_kit', '-i', in_file, '-o', '/root'],
        ['download_kit', '-i', 'notValidRoot', '-o', str(tmpdir)]
    ]
    monkeypatch.setattr(sys_arg, args[0])
    with pytest.raises(PermissionError):
        argument_parser()

    monkeypatch.setattr(sys_arg,args[1])
    with pytest.raises(SystemExit):
        argument_parser()

def test_download(monkeypatch, in_file, tmpdir):
    arg=['download_kit', '-i', in_file, '-o', str(tmpdir)]
    monkeypatch.setattr(sys_arg, arg)
    main()
