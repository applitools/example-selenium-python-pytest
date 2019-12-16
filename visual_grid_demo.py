from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome

from applitools.selenium import (
    logger,
    VisualGridRunner,
    Eyes,
    Target,
    Configuration,
    BatchInfo,
    BrowserType,
    DeviceName,
)

# Create a runner with concurrency of 10
visual_grid_runner = VisualGridRunner(10)
# Initialize Eyes with Visual Grid Runner
eyes = Eyes(visual_grid_runner)

# Create a new Webdriver, ChromeDriverManager is uses for detect or download the chromedriver
driver = Chrome(ChromeDriverManager().install())
logger.set_logger(logger.StdoutLogger())

# Create SeleniumConfiguration.
conf = (Configuration()
        .set_api_key("YOU API KEY")
        .set_app_name("Blank App")
        .set_test_name("Smoke Test via Visual Grid")
        .set_batch(BatchInfo("VIP Browser combo batch"))
        .add_browser(800, 600, BrowserType.CHROME)
        .add_browser(700, 500, BrowserType.CHROME)
        .add_browser(1200, 800, BrowserType.FIREFOX)
        .add_browser(1600, 1200, BrowserType.FIREFOX)
        .add_device_emulation(DeviceName.iPhone_4))

# Set the configuration object to eyes
eyes.set_configuration(conf)

try:
    # Navigate to the URL we want to test
    driver.get("https://demo.applitools.com")

    # Call Open on eyes to initialize a test session
    eyes.open(driver)

    # Check the Login page
    eyes.check("Step 1 - Login page", Target.window().fully())

    # Click on the Login button to go to the App's main page
    driver.find_element_by_id("log-in").click()

    # Check the App page
    eyes.check("Step 2 - App Page", Target.window().fully())

    print(
        "Please wait... we are now: \n1. Uploading resources, \n2. Rendering in Visual Grid, "
        "and \n3. Using Applitools A.I. to validate the checkpoints. \nIt'll take about 30 "
        "secs to a minute...")

    # Send close task
    eyes.close_async()
except Exception as e:
    print(str(e))
    # If the test was aborted before eyes.close / eyes.close_async was called, ends the test
    # as aborted.
    eyes.abort()
finally:
    driver.quit()
    results = visual_grid_runner.get_all_test_results()
    print(results)
