from applitools.selenium import Eyes, Target
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def test_log_into_bank_account(webdriver: Chrome, eyes: Eyes) -> None:

  # Load the login page.
  webdriver.get("https://demo.applitools.com")

  # Verify the full login page loaded correctly.
  eyes.check(Target.window().fully().with_name("Login page"))

  # Perform login.
  webdriver.find_element(By.ID, "username").send_keys("applibot")
  webdriver.find_element(By.ID, "password").send_keys("I<3VisualTests")
  webdriver.find_element(By.ID, "log-in").click()

  # Verify the full main page loaded correctly.
  # This snapshot uses LAYOUT match level to avoid differences in closing time text.
  eyes.check(Target.window().fully().with_name("Main page").layout())
