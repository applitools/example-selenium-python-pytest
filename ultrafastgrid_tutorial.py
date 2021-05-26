import os
import pytest

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from applitools.selenium import (
    VisualGridRunner,
    Eyes,
    Target,
    BatchInfo,
    BrowserType,
    DeviceName,
)


@pytest.fixture(scope="module")
def batch_info():
    """
    Use one BatchInfo for all tests inside module
    """
    return BatchInfo("Ultrafast Batch")


@pytest.fixture(name="driver", scope="function")
def driver_setup():
    """
    New browser instance per test and quite.
    """
    # Set chrome driver to headless when running on the CI
    options = webdriver.ChromeOptions()
    options.headless = (os.getenv('CI', 'False') == 'true')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    yield driver
    # Close the browser.
    driver.quit()


@pytest.fixture(name="runner", scope="session")
def runner_setup():
    """
    One test runner for all tests. Print test results in the end of execution.
    """
    runner = VisualGridRunner()
    yield runner
    all_test_results = runner.get_all_test_results()
    print(all_test_results)


@pytest.fixture(name="eyes", scope="function")
def eyes_setup(runner, batch_info):
    """
    Basic Eyes setup. It'll abort test if wasn't closed properly.
    """
    eyes = Eyes(runner)
    # Initialize the eyes SDK and set your private API key.
    eyes.api_key = os.environ["APPLITOOLS_API_KEY"]
    eyes.configure.batch = batch_info

    # Add browsers with different viewports
    # Add mobile emulation devices in Portrait mode
    (
        eyes.configure.add_browser(800, 600, BrowserType.CHROME)
            .add_browser(700, 500, BrowserType.FIREFOX)
            .add_browser(1600, 1200, BrowserType.IE_11)
            .add_browser(1024, 768, BrowserType.EDGE_CHROMIUM)
            .add_browser(800, 600, BrowserType.SAFARI)
            .add_device_emulation(DeviceName.iPhone_X)
            .add_device_emulation(DeviceName.Pixel_2)
    )

    yield eyes
    # If the test was aborted before eyes.close was called, ends the test as aborted.
    eyes.abort_if_not_closed()


def test_ultra_fast(eyes, driver):
    # Navigate to the url we want to test
    driver.get("https://demo.applitools.com")

    # Call Open on eyes to initialize a test session
    eyes.open(driver, "Demo App - Python - UFG", "Ultrafast grid demo", {"width": 800, "height": 600})

    # check the login page with fluent api, see more info here
    # https://applitools.com/docs/topics/sdk/the-eyes-sdk-check-fluent-api.html
    eyes.check("", Target.window().fully().with_name("Login page"))

    driver.find_element_by_id("log-in").click()

    # Check the app page
    eyes.check("", Target.window().fully().with_name("App page"))

    # Call Close on eyes to let the server know it should display the results
    eyes.close(False)
