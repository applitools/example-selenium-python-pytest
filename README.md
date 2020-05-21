# Eyes Python Selenium Ultrafastgrid Tutorial

## Pre-requisites:

1. Python 3 is installed on your machine.
   * [Install Python 3.](https://realpython.com/installing-python/)
2. Package manager pip is installed on your machine.
   * [Install pip](https://pip.pypa.io/en/stable/installing/)
3. Chrome browser is installed on your machine.

   * [Install Chrome browser](https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=en&oco=0)
4. Chrome Webdriver is on your machine and is in the environment variable PATH. Here are some resources from the internet that'll help you.
   * [Download Chrome Webdriver](https://chromedriver.chromium.org/downloads)
   * https://splinter.readthedocs.io/en/0.1/setup-chrome.html
   * https://stackoverflow.com/questions/38081021/using-selenium-on-mac-chrome
   * https://www.youtube.com/watch?time_continue=182&v=dz59GsdvUF8
5. Git is installed on your machine. 

   * [Install git](https://www.atlassian.com/git/tutorials/install-git)
6. If you want to run example from IDE, install any IDE for Python (e.g. [PyCharm](https://www.jetbrains.com/pycharm/download/) )
7. Restart your machine to implement updated  environment variables (need for some OS).

## Steps to run this example

1. Git clone this repo

`git clone https://github.com/applitools/tutorial-selenium-python-ultrafastgrid.git`, or download [this as a Zip file](https://github.com/applitools/tutorial-selenium-python-ultrafastgrid/archive/master.zip) and unzip it

2. Get an API key by logging into Applitools > Person Icon > My API Key
3. Navigate to just cloned folder tutorial-selenium-python-ultrafastgrid
4. Open in any editor file ultrafastgrid_demo.py  and set your ApiKey in string '.set_api_key('...')' (or comment the string and set APPLITOOLS_API_KEY environment variable)
5. Install requirements `pip install -r requirements.txt`
6. Run `ultrafastgrid_demo.py` by calling `python ultrafastgrid_demo.py` 
7. If you want run from IDE - start PyCharm, open just cloned project, set project interpreter by File > Settings > Project: > Project Interpreter  choose interpreter by dropdown box; tap Run and choose 'ultrafastgrid_demo'.

Read more here: https://www.applitools.com/tutorials/selenium-python.html