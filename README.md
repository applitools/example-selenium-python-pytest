# Applitools Tutorial: Selenium Python pytest with the Ultrafast Grid

This is the example project for the [Selenium Python pytest tutorial](https://applitools.com/tutorials/quickstart/web/selenium/python).
It shows how to start automating visual tests
with [Applitools Eyes](https://applitools.com/platform/eyes/)
and the [Ultrafast Grid](https://applitools.com/platform/ultrafast-grid/)
using [Selenium](https://www.selenium.dev/) in Python.

It uses:

* [Python](https://www.python.org/) as the programming language
* [Selenium WebDriver](https://www.selenium.dev/) for browser automation
* [pytest](https://docs.pytest.org/) as the core test framework
* [Google Chrome](https://www.google.com/chrome/downloads/) as the local browser for testing
* [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) for dependency management
* [Applitools Eyes](https://applitools.com/platform/eyes/) for visual testing
* [Applitools Ultrafast Grid](https://applitools.com/platform/ultrafast-grid/) for cross-browser execution

To run this example project, you'll need:

1. An [Applitools account](https://auth.applitools.com/users/register), which you can register for free
2. A recent version of [Python 3](https://www.python.org/)
3. A good Python editor like [Visual Studio Code](https://code.visualstudio.com/docs/languages/python)
   or [PyCharm](https://www.jetbrains.com/pycharm/).
4. An up-to-date version of [Google Chrome](https://www.google.com/chrome/downloads/).
5. A corresponding version of [ChromeDriver](https://chromedriver.chromium.org/downloads).

To install dependencies, run:

```
pip install -r requirements.txt
```

The main test case spec is [`test_acme_bank.py`](tests/test_acme_bank.py).

To execute tests, set the `APPLITOOLS_API_KEY` environment variable
to your [account's API key](https://applitools.com/tutorials/getting-started/setting-up-your-environment.html),
and then run:

```
python3 -m pytest -s -v tests
```

**For full instructions on running this project, take our
[Selenium Python pytest tutorial](https://applitools.com/tutorials/quickstart/web/selenium/python)!**
