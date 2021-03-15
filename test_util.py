import time


from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

import unittest
from django.test import TestCase, Client
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

# from django.test.utils import setup_test_environment
import pytest

from selenium import webdriver

# from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


DEFAULT_TIMEOUT_S = 23
SEARCH_TIMEOUT_S = 180
DISABLE_TEST = True


def create_webdriver():
    """
    Create browser webdriver
    """

    chromeOptions = Options()
    chromeOptions.headless = True

    # base = os.path.dirname(settings.BASE_DIR)
    # with webdriver.Chrome(executable_path=os.path.join(base, 'chromedriver.exe')) as driver:
    browser = webdriver.Chrome(
        executable_path="/home/travis/virtualenv/python3.8/bin/chromedriver",
        options=chromeOptions,
    )
    browser.get("http://linuxhint.com")
    print("Title: %s" % browser.title)
    # browser.quit()
    # browser.implicitly_wait(10)
    # time.sleep(1)

    return browser


def build_full_url(obj, relative_url_name, kwargs=None):
    """
    Build full url from domain root and with specified reltive part
    """
    return obj.live_server_url + reverse(relative_url_name, kwargs=kwargs)


def create_user():
    """
    Create a dummy user
    """

    pwd = "dummy_pwd"
    email = "user@dummy.com"
    username = email
    user = get_user_model().objects.create_user(username, email, pwd)
    # print('Dummy user {} is created for test: {}'.format(user, user != None))

    return user, pwd


def sign_in_user_into_webdriver(obj, user, password, driver, relative_url):

    print("COOKIE_X", obj.client.cookies, "THERE_IS_X", obj.client.session, "OFF_X")
    # sign-in user
    obj.client.login(username=user.username, password=password)

    # share session to webdriver
    # [TODO] Check doc or forum to understand why it is mandatory to load session
    print("COOKIE_A", obj.client.cookies, "THERE_IS", obj.client.session, "OFF")
    cookie = obj.client.cookies["sessionid"]
    print("COOKIE_B", cookie)
    driver.get(
        build_full_url(obj, relative_url)
    )  # selenium will set cookie domain based on current page domain
    driver.add_cookie(
        {"name": "sessionid", "value": cookie.value, "secure": False, "path": "/"}
    )
    driver.refresh()  # need to update page for logged in user
