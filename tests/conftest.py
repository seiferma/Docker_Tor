import pytest

@pytest.fixture(scope='session')
def img_name(pytestconfig):
    return 'test-image'
