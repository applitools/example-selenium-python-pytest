import os
import pytest

from applitools.selenium import *
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope='session')
def api_key():
  return os.getenv('APPLITOOLS_API_KEY')


@pytest.fixture(scope='session')
def headless():
  h = os.getenv('HEADLESS', default='false')
  return h.lower() == 'true'


@pytest.fixture(scope='session')
def runner():
  run = VisualGridRunner(RunnerOptions().test_concurrency(5))
  yield run
  print(run.get_all_test_results())


@pytest.fixture(scope='session')
def batch_info():
  return BatchInfo("Example: Selenium Python pytest with the Ultrafast Grid")


@pytest.fixture(scope='session')
def configuration(api_key: str, batch_info: BatchInfo):
  config = Configuration()
  config.set_batch(batch_info)
  config.set_api_key(api_key)
  config.add_browser(800, 600, BrowserType.CHROME)
  config.add_browser(1600, 1200, BrowserType.FIREFOX)
  config.add_browser(1024, 768, BrowserType.SAFARI)
  config.add_device_emulation(DeviceName.Pixel_2, ScreenOrientation.PORTRAIT)
  config.add_device_emulation(DeviceName.Nexus_10, ScreenOrientation.LANDSCAPE)
  return config


@pytest.fixture(scope='session')
def chromedriver_service():
  path = ChromeDriverManager().install()
  return Service(path)


@pytest.fixture(scope='function')
def webdriver(headless: bool, chromedriver_service: Service):
  options = ChromeOptions()
  options.headless = headless
  driver = Chrome(service=chromedriver_service, options=options)
  yield driver
  driver.quit()


@pytest.fixture(scope='function')
def eyes(
  runner: VisualGridRunner,
  configuration: Configuration,
  webdriver: Chrome,
  request: pytest.FixtureRequest):

  eyes = Eyes(runner)
  eyes.set_configuration(configuration)
  eyes.open(
    driver=webdriver,
    app_name='ACME Bank Web App',
    test_name=request.node.name,
    viewport_size=RectangleSize(1024, 768))
  
  yield eyes
  eyes.close_async()
