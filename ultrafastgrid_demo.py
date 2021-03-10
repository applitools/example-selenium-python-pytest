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


def set_up(eyes):

    # You can get your api key from the Applitools dashboard
    eyes.configure.set_api_key("APPLITOOLS_API_KEY")

    # create a new batch info instance and set it to the configuration
    eyes.configure.set_batch(BatchInfo("Ultrafast Batch"))

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


def ultra_fast_test(web_driver, eyes):
    try:
        # Navigate to the url we want to test
        web_driver.get("https://demo.applitools.com")

        # Call Open on eyes to initialize a test session
        eyes.open(
            web_driver, "Demo App - python", "Ultrafast grid demo", {"width": 800, "height": 600}
        )

        # check the login page with fluent api, see more info here
        # https://applitools.com/docs/topics/sdk/the-eyes-sdk-check-fluent-api.html
        eyes.check("", Target.window().fully().with_name("Login page"))

        web_driver.find_element_by_id("log-in").click()

        # Check the app page
        eyes.check("", Target.window().fully().with_name("App page"))

        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()
    except Exception as e:
        eyes.abort_async()
        print(e)


def tear_down(web_driver, runner):
    # Close the browser
    web_driver.quit()

    # we pass false to this method to suppress the exception that is thrown if we
    # find visual differences
    all_test_results = runner.get_all_test_results()
    print(all_test_results)


# Create a new chrome web driver
web_driver = Chrome(ChromeDriverManager().install())

# Create a runner with concurrency of 1
runner = VisualGridRunner(1)

# Create Eyes object with the runner, meaning it'll be a Visual Grid eyes.
eyes = Eyes(runner)

set_up(eyes)

try:
    # ⭐️ Note to see visual bugs, run the test using the above URL for the 1st run.
    # but then change the above URL to https://demo.applitools.com/index_v2.html
    # (for the 2nd run)
    ultra_fast_test(web_driver, eyes)
finally:
    tear_down(web_driver, runner)
