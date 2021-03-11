"""
    *
    * Test constants
    *
    *
"""
test_ftp_url_1="ftp://sample.com/sometextfile.txt"
test_sftp_url_1="sftp://sample.com/somedir/somefile.txt"
test_http_url1="http://sample.com/files/test_complete.txt"
test_https_url1="https://sample.com/files/somesecurefile.txt"


sys_arg='sys.argv'

test_ftp_url="ftp://speedtest.tele2.net/1KB.zip"
test_http_url="http://speedtest.ftp.otenet.gr/files/test10k.db"


http_url_file_name= "test10k.db"
http_url1_file_name= "test_complete.txt"
https_url1_file_name= "somesecurefile.txt"

test_ftp_url_file_name= "1KB.zip"
test_ftp_url_1_file_name="sometextfile.txt"

content_type='Content-Type'
type_parm='application/json; charset=utf-8'
host='localhost'
http_protocol='http'
content= b'\x00\x00\x00\x00\x00\x00\x00\x00'
empty_content=b''


ftp_module_path='downloadKit.protocol_factory.ftp.ftpUrlDownloader.execute'