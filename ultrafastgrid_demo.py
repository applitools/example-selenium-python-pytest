from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
import os


from applitools.selenium import (
    logger,
    VisualGridRunner,
    Eyes,
    Target,

    BatchInfo,
    BrowserType,
    DeviceName,
)

# Create a new Webdriver, ChromeDriverManager is uses for detect or download the chromedriver
driver = Chrome(ChromeDriverManager().install())

# Create a runner with concurrency of 10
ultrafast_grid_runner = VisualGridRunner(10)
# Initialize Eyes with Ultrafast Grid Runner
eyes = Eyes(ultrafast_grid_runner)

logger.set_logger(logger.StdoutLogger())

# Create SeleniumConfiguration.
(
    eyes.configure
        .set_api_key('APPLITOOLS_API_KEY') # Set APPLITOOLS_API_KEY here or as env var and use "os.environ['APPLITOOLS_API_KEY']"
        .set_batch(BatchInfo("Py Ultrafast Batch"))
        .add_browser(800, 600, BrowserType.CHROME)
        .add_browser(700, 500, BrowserType.FIREFOX)
        .add_browser(1600, 1200, BrowserType.IE_11)
        .add_browser(1024, 768, BrowserType.EDGE_CHROMIUM)
        .add_browser(800, 600, BrowserType.SAFARI)
        .add_device_emulation(DeviceName.iPhone_X)
        .add_device_emulation(DeviceName.Pixel_2)
)


try:
    # ⭐️ Note to see visual bugs, run the test using the above URL for the 1st run.
    # but then change the above URL to https://demo.applitools.com/index_v2.html    (for the 2nd run)
    # Navigate to the URL we want to test
    driver.get("https://demo.applitools.com")

    # Call Open on eyes to initialize a test session
    eyes.open(driver, "Demo App", "Ultrafast grid demo")

    # check the login page with fluent api, see more info here
    # https://applitools.com/docs/topics/sdk/the-eyes-sdk-check-fluent-api.html
    eyes.check("Login page", Target.window().fully())

    # Click on the Login button to go to the App's main page
    driver.find_element_by_id("log-in").click()

    # Check the App page
    eyes.check("App Page", Target.window().fully())

    print(
        "Please wait... we are now: \n1. Uploading resources, \n2. Rendering in Ultrafast Grid, "
        "and \n3. Using Applitools A.I. to validate the checkpoints. \nIt'll take about 30 "
        "secs to a minute..."
    )

    # Call Close on eyes to let the server know it should display the results
    eyes.close_async()
except Exception as e:
    print(str(e))
finally:
    # Close the browser
    driver.quit()
    # we pass false to this method to suppress the exception that is thrown if we find visual differences
    results = ultrafast_grid_runner.get_all_test_results(False)
    # Print results
    print(results)
    # If the test was aborted before eyes.close / eyes.close_async was called, ends the test
    # as aborted.
    eyes.abort_async()
