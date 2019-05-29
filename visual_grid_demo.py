from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome

from applitools.selenium import (
    VisualGridRunner,
    Eyes,
    Target,
    Configuration,
    BatchInfo,
    BrowserType,
    DeviceName,
)


def initialize_eyes(runner):
    eyes = Eyes(runner)
    # Set API key
    eyes.api_key = "YOU API KEY"

    # If dedicated or on-prem cloud, uncomment and enter the cloud url
    # Default: https://eyes.applitools.com
    # eyes.server_url = "https://testeyes.applitools.com"

    # Create SeleniumConfiguration.
    sconf = Configuration()

    # Set the AUT name
    sconf.app_name = "Blank App"

    # Set a test name
    sconf.test_name = "Smoke Test via Visual Grid"

    #  Set a batch name so all the different browser and mobile combinations are
    #  part of the same batch
    sconf.batch = BatchInfo("VIP Browser combo batch")

    # Add Chrome browsers with different Viewports
    sconf.add_browser(800, 600, BrowserType.CHROME)
    sconf.add_browser(700, 500, BrowserType.CHROME)

    # Add Firefox browser with different Viewports
    sconf.add_browser(1200, 800, BrowserType.FIREFOX)
    sconf.add_browser(1600, 1200, BrowserType.FIREFOX)

    # Add iPhone 4 device emulation
    sconf.add_device_emulation(DeviceName.iPhone_4)

    # Set the configuration object to eyes
    eyes.configuration = sconf
    return eyes


def run_test():
    # Create a runner with concurrency of 10
    runner = VisualGridRunner(10)

    # Initialize Eyes with Visual Grid Runner
    eyes = initialize_eyes(runner)

    # Create a new Webdriver, ChromeDriverManager is uses for detect or download the chromedriver
    driver = Chrome(ChromeDriverManager().install())

    # Navigate to the URL we want to test
    driver.get("https://demo.applitools.com")

    # To see visual bugs, change the above URL to:
    # driver.get("https://demo.applitools.com/index_v2.html")
    # https://demo.applitools.com/index_v2.html and run the test again

    # Call Open on eyes to initialize a test session
    eyes.open(driver)

    # Check the Login page
    eyes.check("Step 1 - Login page", Target.window().fully())

    # Click on the Login button to go to the App's main page
    driver.find_element_by_id("log-in").click()

    # Check the App page
    eyes.check("Step 2 - App Page", Target.window().fully())

    driver.quit()
    print(
        "Please wait... we are now: \n1. Uploading resources, \n2. Rendering in Visual Grid, "
        "and \n3. Using Applitools A.I. to validate the checkpoints. \nIt'll take about 30 "
        "secs to a minute..."
    )

    # Close eyes and collect results
    # This could be used instead of close_async and get_all_test_results
    # eyes.close()

    # Send close task
    eyes.close_async()

    # Return test results from all eyes instances
    all_test_results = runner.get_all_test_results()
    print(all_test_results)


if __name__ == "__main__":
    run_test()
