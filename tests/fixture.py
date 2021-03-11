import pytest
import os
import random
import string

from tests.contansts import test_http_url,test_ftp_url


@pytest.fixture(scope='session')
def input_urls():
    return [(test_http_url,),(test_ftp_url,)]

@pytest.fixture(scope='session')
def in_file(input_urls):
    file = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    with open(file, 'w') as f:
        for url in input_urls:
            url = url[0]
            f.write(url + '\n')
    yield os.path.abspath(file)
    os.remove(file)



