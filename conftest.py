from fixture.application import Application
import pytest


fixture = None


@pytest.fixture
def app(request):
    global fixture
    if fixture is None or not fixture.fixture_is_valid():
        base_url = request.config.getoption("--baseUrl")
        fixture = Application(base_url=base_url)
    return fixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--baseUrl", action="store", default="https://fc.frfrstaging.pw/login")