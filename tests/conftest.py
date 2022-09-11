"""
This module provides fixtures for test setup.
You can use these fixtures for all tests in your suite.
You could also copy-paste this module into your own test project to provide Applitools setup for your tests.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import os
import pytest

from applitools.selenium import *
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


# --------------------------------------------------------------------------------
# Session-Scope Fixtures
#   These fixtures run one time for the whole test suite.
#   Subsequent calls use the value cached from the first execution.
# --------------------------------------------------------------------------------

@pytest.fixture(scope='session')
def api_key():
  """
  Reads the Applitools API key from an environment variable.
  """
  return os.getenv('APPLITOOLS_API_KEY')


@pytest.fixture(scope='session')
def headless():
  """
  Reads the headless mode setting from an environment variable.
  Uses headless mode for Continuous Integration (CI) execution.
  Uses headed mode for local development.
  """
  h = os.getenv('HEADLESS', default='false')
  return h.lower() == 'true'


@pytest.fixture(scope='session')
def runner():
  """
  Creates the runner for the Ultrafast Grid.
  Concurrency refers to the number of visual checkpoints Applitools will perform in parallel.
  Warning: If you have a free account, then concurrency will be limited to 1.
  After the test suite finishes execution, closes the batch and report visual differences to the console.
  Note that it forces pytest to wait synchronously for all visual checkpoints to complete.
  """
  run = VisualGridRunner(RunnerOptions().test_concurrency(5))
  yield run
  print(run.get_all_test_results())


@pytest.fixture(scope='session')
def batch_info():
  """
  Creates a new batch for tests.
  A batch is the collection of visual checkpoints for a test suite.
  Batches are displayed in the dashboard, so use meaningful names.
  """
  return BatchInfo("Example: Selenium Python pytest with the Ultrafast Grid")


@pytest.fixture(scope='session')
def configuration(api_key: str, batch_info: BatchInfo):
  """
  Creates a configuration for Applitools Eyes to test 3 desktop browsers and 2 mobile devices.
  """

  # Construct the object
  config = Configuration()

  # Set the batch for the config.
  config.set_batch(batch_info)

  # Set the Applitools API key so test results are uploaded to your account.
  # If you don't explicitly set the API key with this call,
  # then the SDK will automatically read the `APPLITOOLS_API_KEY` environment variable to fetch it.
  config.set_api_key(api_key)

  # Add 3 desktop browsers with different viewports for cross-browser testing in the Ultrafast Grid.
  # Other browsers are also available, like Edge and IE.
  config.add_browser(800, 600, BrowserType.CHROME)
  config.add_browser(1600, 1200, BrowserType.FIREFOX)
  config.add_browser(1024, 768, BrowserType.SAFARI)

  # Add 2 mobile emulation devices with different orientations for cross-browser testing in the Ultrafast Grid.
  # Other mobile devices are available, including iOS.
  config.add_device_emulation(DeviceName.Pixel_2, ScreenOrientation.PORTRAIT)
  config.add_device_emulation(DeviceName.Nexus_10, ScreenOrientation.LANDSCAPE)

  # Return the configuration object
  return config


@pytest.fixture(scope='session')
def chromedriver_service():
  """
  Sets up ChromeDriver and returns a Service object for initializing WebDriver objects.
  """
  path = ChromeDriverManager().install()
  return Service(path)


# --------------------------------------------------------------------------------
# Function-Scope Fixtures
#   These fixtures run one time before each test that calls them.
#   Returned values are not cached and reused across different tests.
# --------------------------------------------------------------------------------

@pytest.fixture(scope='function')
def webdriver(headless: bool, chromedriver_service: Service):
  """
  Creates a WebDriver object for Chrome.
  Even though this test will run visual checkpoints on different browsers in the Ultrafast Grid,
  it still needs to run the test one time locally to capture snapshots.
  After the test function finishes execution, quits the browser.
  """
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
  """
  Creates the Applitools Eyes object connected to the VisualGridRunner and set its configuration.
  Then, opens Eyes to start visual testing before the test, and closes Eyes at the end of the test.
  """

  eyes = Eyes(runner)
  eyes.set_configuration(configuration)

  eyes.open(
    driver=webdriver,
    app_name='ACME Bank Web App',
    test_name=request.node.name,
    viewport_size=RectangleSize(1024, 768))
  
  yield eyes
  eyes.close_async()
