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
from applitools.selenium.runner import EyesRunner
from selenium.webdriver import Chrome, ChromeOptions, Remote


# --------------------------------------------------------------------------------
# Runner Settings
#   These could be set by environment variables or other input mechanisms.
#   They are hard-coded here to keep the example project simple.
# --------------------------------------------------------------------------------

USE_ULTRAFAST_GRID = True
USE_EXECUTION_CLOUD = False


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
  Creates the runner for either the Ultrafast Grid or the Classic runner (local execution).
  For UFG, concurrency refers to the number of visual checkpoints Applitools will perform in parallel.
  Warning: If you have a free account, then concurrency will be limited to 1.
  After the test suite finishes execution, closes the batch and report visual differences to the console.
  Note that it forces pytest to wait synchronously for all visual checkpoints to complete.
  """

  if USE_ULTRAFAST_GRID:
    run = VisualGridRunner(RunnerOptions().test_concurrency(5))
  else:
    run = ClassicRunner()
  
  yield run
  print(run.get_all_test_results())


@pytest.fixture(scope='session')
def batch_info():
  """
  Creates a new batch for tests.
  A batch is the collection of visual checkpoints for a test suite.
  Batches are displayed in the Eyes Test Manager, so use meaningful names.
  """
  
  runner_name = "Ultrafast Grid" if USE_ULTRAFAST_GRID else "Classic runner"
  return BatchInfo(f"Example: Selenium Python pytest with the {runner_name}")


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

  # If running tests on the Ultrafast Grid, configure browsers.
  if USE_ULTRAFAST_GRID:

    # Add 3 desktop browsers with different viewports for cross-browser testing in the Ultrafast Grid.
    # Other browsers are also available, like Edge and IE.
    config.add_browser(800, 600, BrowserType.CHROME)
    config.add_browser(1600, 1200, BrowserType.FIREFOX)
    config.add_browser(1024, 768, BrowserType.SAFARI)

    # Add 2 mobile browsers with different orientations for cross-browser testing in the Ultrafast Grid.
    # Other mobile devices are available.
    config.add_browser(IosDeviceInfo(IosDeviceName.iPhone_11, ScreenOrientation.PORTRAIT))
    config.add_browser(ChromeEmulationInfo(DeviceName.Nexus_10, ScreenOrientation.LANDSCAPE))

  # Return the configuration object
  return config


# --------------------------------------------------------------------------------
# Function-Scope Fixtures
#   These fixtures run one time before each test that calls them.
#   Returned values are not cached and reused across different tests.
# --------------------------------------------------------------------------------

@pytest.fixture(scope='function')
def webdriver(headless: bool):
  """
  Creates a WebDriver object for Chrome.
  After the test function finishes execution, quits the browser.
  """

  options = ChromeOptions()
  options.add_argument("--headless=new")

  if USE_EXECUTION_CLOUD:
    driver = Remote(
      command_executor=Eyes.get_execution_cloud_url(),
      options=options)
  else:
    driver = Chrome(options=options)
  
  yield driver
  driver.quit()


@pytest.fixture(scope='function')
def eyes(
  runner: EyesRunner,
  configuration: Configuration,
  webdriver: Remote,
  request: pytest.FixtureRequest):
  """
  Creates the Applitools Eyes object connected to the runner and set its configuration.
  Then, opens Eyes to start visual testing before the test, and closes Eyes at the end of the test.
  
  Opening Eyes requires 4 arguments:
    1. The WebDriver object to "watch".
    2. The name of the application under test.
       All tests for the same app should share the same app name.
       Set this name wisely: Applitools features rely on a shared app name across tests.
    3. The name of the test case for the given application.
       Additional unique characteristics of the test may also be specified as part of the test name,
       such as localization information ("Home Page - EN") or different user permissions ("Login by admin").
    4. The viewport size for the local browser.
       Eyes will resize the web browser to match the requested viewport size.
       This parameter is optional but encouraged in order to produce consistent results.
  """

  eyes = Eyes(runner)
  eyes.set_configuration(configuration)

  eyes.open(
    driver=webdriver,
    app_name='ACME Bank Web App',
    test_name=request.node.name,
    viewport_size=RectangleSize(1200, 600))
  
  yield eyes
  eyes.close_async()
