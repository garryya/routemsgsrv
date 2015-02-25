import pytest


def pytest_addoption(parser):
    parser.addoption("--server", action="store", dest='server', default='localhost', help="test server IP")

@pytest.fixture
def server(request):
    return request.config.getoption("--server")


def pytest_runtest_setup(item):
    pass
